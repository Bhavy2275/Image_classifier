"""
Inference pipeline: image bytes → top-K class predictions.

Uses OpenCLIP zero-shot classification (ViT-B-32, LAION-2B) as the primary classifier.
Falls back to EfficientNetV2-S (timm) if CLIP is unavailable.
"""
from __future__ import annotations

import io
import logging
from functools import lru_cache
from typing import List, Optional

import numpy as np
import torch
from PIL import Image
from timm.data import create_transform, resolve_model_data_config

from app.ml.labels import get_imagenet_labels
from app.ml.model import get_torch_model
from app.schemas.prediction import TopKClass

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def get_image_transform():
    """Return the official preprocessing transform for EfficientNetV2-S (Grad-CAM use only)."""
    model = get_torch_model()
    config = resolve_model_data_config(model)
    return create_transform(**config)


def preprocess_image_tensor(image_bytes: bytes) -> torch.Tensor:
    """Preprocess image bytes into a normalized PyTorch tensor for EfficientNetV2-S."""
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    transform = get_image_transform()
    tensor = transform(img).unsqueeze(0)
    return tensor


def preprocess_image(image_bytes: bytes) -> np.ndarray:
    """Preprocess image bytes into a numpy array."""
    tensor = preprocess_image_tensor(image_bytes)
    return tensor.cpu().numpy()


def softmax(logits: np.ndarray) -> np.ndarray:
    exp = np.exp(logits - logits.max())
    return exp / exp.sum()


def run_inference(session: Optional[object], image_bytes: bytes, top_k: int = 5) -> List[TopKClass]:
    """
    Run zero-shot classification using OpenCLIP (primary) or EfficientNetV2-S (fallback).
    """
    # ── Primary: OpenCLIP zero-shot ──────────────────────────────────────
    try:
        from app.ml.clip_classifier import clip_classify
        results = clip_classify(image_bytes, top_k=top_k)
        return [
            TopKClass(
                rank=rank + 1,
                class_index=int(idx),
                label=label,
                confidence=float(round(conf, 6)),
            )
            for rank, (idx, label, conf) in enumerate(results)
        ]
    except Exception as exc:
        logger.warning(f"CLIP inference failed ({exc}), falling back to EfficientNetV2-S...")

    # ── Fallback: EfficientNetV2-S (timm) ───────────────────────────────
    labels = get_imagenet_labels()
    tensor = preprocess_image_tensor(image_bytes)
    model = get_torch_model()

    with torch.no_grad():
        output = model(tensor)
        logits = output.cpu().numpy()[0]

    probs = softmax(logits)
    top_indices = probs.argsort()[::-1][:top_k]

    return [
        TopKClass(
            rank=rank + 1,
            class_index=int(idx),
            label=labels.get(int(idx), f"class_{idx}"),
            confidence=float(round(probs[idx], 6)),
        )
        for rank, idx in enumerate(top_indices)
    ]
