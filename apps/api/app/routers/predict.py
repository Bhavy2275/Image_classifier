"""
Single-image inference endpoint.

POST /predict
  - Accepts: multipart/form-data with an `image` file field
  - Optionally: `include_heatmap=true` to include Grad-CAM base64 PNG
  - Returns: PredictionResult JSON
"""
from __future__ import annotations

import time
import logging
from typing import Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status

from app.ml.inference import run_inference
from app.ml.gradcam import generate_gradcam
from app.ml.model import get_model_session
from app.routers.auth import get_current_user
from app.schemas.prediction import PredictionResult
from app.services import cloudinary_service, supabase_service
from app.config import get_settings

logger = logging.getLogger(__name__)
router = APIRouter()

_ALLOWED_MIME = {"image/jpeg", "image/png", "image/webp", "image/gif"}
_MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


@router.post("/predict", response_model=PredictionResult)
async def predict(
    image: UploadFile = File(..., description="Image to classify (JPEG/PNG/WebP)"),
    include_heatmap: bool = Form(True, description="Include Grad-CAM heatmap in response"),
    user: Optional[dict] = Depends(get_current_user),
):
    """
    Run EfficientNet-B0 inference on a single image.

    Returns the top-5 predicted ImageNet classes with confidence scores
    and an optional Grad-CAM heatmap as a base64-encoded PNG.
    """
    # ── Validation ──────────────────────────────────────────
    if image.content_type not in _ALLOWED_MIME:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Unsupported file type: {image.content_type}. Allowed: {_ALLOWED_MIME}",
        )

    image_bytes = await image.read()
    if len(image_bytes) > _MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="Image must be smaller than 10 MB.",
        )

    start = time.perf_counter()

    # ── Upload to Cloudinary ─────────────────────────────────
    image_url, cloudinary_public_id = cloudinary_service.upload_image(
        image_bytes, filename=image.filename
    )

    # ── ONNX Inference ───────────────────────────────────────
    settings = get_settings()
    session = get_model_session()
    top_classes = run_inference(session, image_bytes, top_k=settings.top_k)

    # ── Grad-CAM ─────────────────────────────────────────────
    heatmap_b64: Optional[str] = None
    if include_heatmap:
        try:
            heatmap_b64 = generate_gradcam(image_bytes, target_class_idx=top_classes[0].class_index)
        except Exception as exc:
            logger.warning(f"Grad-CAM generation failed: {exc}")

    elapsed_ms = (time.perf_counter() - start) * 1000

    # ── Persist to Supabase ──────────────────────────────────
    user_id = user.get("sub") if user else None
    prediction_id = await supabase_service.insert_prediction(
        user_id=user_id,
        image_url=image_url,
        cloudinary_public_id=cloudinary_public_id,
        top_classes=top_classes,
        heatmap_url=None,  # heatmap returned inline; could also upload to Cloudinary
    )

    return PredictionResult(
        prediction_id=prediction_id,
        image_url=image_url,
        top_classes=top_classes,
        heatmap_base64=heatmap_b64,
        processing_time_ms=round(elapsed_ms, 2),
    )
