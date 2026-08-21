"""
RQ worker task: process a single image within a batch job.

This module is imported by the RQ worker process (not the FastAPI app).
"""
from __future__ import annotations

import logging
from typing import Optional

from app.ml.gradcam import generate_gradcam
from app.ml.inference import run_inference
from app.ml.model import get_model_session
from app.schemas.batch import BatchJobItem, BatchJobStatus
from app.services import cloudinary_service, supabase_service
from app.config import get_settings

logger = logging.getLogger(__name__)


def process_batch_image(
    job_id: str,
    image_bytes: bytes,
    filename: str,
    user_id: Optional[str],
    image_index: int,
) -> dict:
    """
    RQ worker function — runs inference + Grad-CAM for a single image.

    Returns a dict compatible with BatchJobItem for serialization.
    Called by RQ worker process; must be importable at the module level.
    """
    import asyncio

    settings = get_settings()

    try:
        # Upload to Cloudinary
        image_url, cloudinary_public_id = cloudinary_service.upload_image(
            image_bytes, filename=filename
        )

        # ONNX inference
        session = get_model_session()
        top_classes = run_inference(session, image_bytes, top_k=settings.top_k)

        # Grad-CAM
        try:
            heatmap_b64 = generate_gradcam(
                image_bytes, target_class_idx=top_classes[0].class_index
            )
        except Exception as exc:
            logger.warning(f"Grad-CAM failed for {filename}: {exc}")
            heatmap_b64 = None

        # Persist to Supabase
        loop = asyncio.new_event_loop()
        prediction_id = loop.run_until_complete(
            supabase_service.insert_prediction(
                user_id=user_id,
                image_url=image_url,
                cloudinary_public_id=cloudinary_public_id,
                top_classes=top_classes,
                batch_job_id=job_id,
            )
        )
        loop.close()

        return BatchJobItem(
            filename=filename,
            status=BatchJobStatus.COMPLETED,
            prediction_id=prediction_id,
            image_url=image_url,
            top_classes=top_classes,
            heatmap_base64=heatmap_b64,
        ).model_dump()

    except Exception as exc:
        logger.error(f"Batch worker error for {filename}: {exc}", exc_info=True)
        return BatchJobItem(
            filename=filename,
            status=BatchJobStatus.FAILED,
            error=str(exc),
        ).model_dump()
