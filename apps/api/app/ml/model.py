"""
ML model loading: EfficientNetV2-S (pretrained on ImageNet-21k, fine-tuned on 1k).

High-accuracy vision backbone with 300x300 native resolution and ~85.2% top-1 accuracy.
"""
from __future__ import annotations

import logging
from functools import lru_cache
from pathlib import Path
from typing import Any, Optional

import timm
import torch
import torch.nn as nn

logger = logging.getLogger(__name__)

_torch_model: Optional[nn.Module] = None
_ort_session: Any = None
_MODEL_NAME = "tf_efficientnetv2_s.in21k_ft_in1k"


def _get_onnx_path() -> Path:
    from app.config import get_settings
    return Path(get_settings().onnx_model_path)


def _build_torch_model() -> nn.Module:
    """Load EfficientNetV2-S with pretrained ImageNet-21k weights via timm."""
    logger.info(f"Loading high-accuracy {_MODEL_NAME} …")
    model = timm.create_model(_MODEL_NAME, pretrained=True, num_classes=1000)
    model.eval()
    return model


@lru_cache(maxsize=1)
def get_torch_model() -> nn.Module:
    """Return singleton PyTorch model."""
    global _torch_model
    if _torch_model is None:
        _torch_model = _build_torch_model()
    return _torch_model


@lru_cache(maxsize=1)
def get_model_session():
    """
    Return singleton ONNX Runtime InferenceSession if available,
    or None to fall back to PyTorch inference.
    """
    try:
        import onnxruntime as ort

        onnx_path = _get_onnx_path()
        if not onnx_path.exists():
            return None

        providers = (
            ["CUDAExecutionProvider", "CPUExecutionProvider"]
            if ort.get_device() == "GPU"
            else ["CPUExecutionProvider"]
        )

        logger.info(f"Loading ONNX session from {onnx_path} (providers: {providers})")
        session = ort.InferenceSession(str(onnx_path), providers=providers)
        return session
    except Exception as exc:
        logger.warning(f"ONNX Runtime session unavailable ({exc}) — using PyTorch backend.")
        return None
