"""
Grad-CAM heatmap generation using the pytorch-grad-cam library on EfficientNetV2-S.

Returns a base64-encoded PNG of the Grad-CAM heatmap blended over the
original image at 50% opacity.
"""
from __future__ import annotations

import base64
import io
from typing import Optional

import numpy as np
import torch
from PIL import Image
from pytorch_grad_cam import GradCAM
from pytorch_grad_cam.utils.image import show_cam_on_image

from app.ml.model import get_torch_model
from app.ml.inference import preprocess_image_tensor, softmax

# EfficientNetV2 conv_head is the last conv layer before global pooling
_TARGET_LAYER_ATTR = "conv_head"


def _get_target_layer(model):
    """Return the target conv layer for Grad-CAM."""
    return getattr(model, _TARGET_LAYER_ATTR)


def generate_gradcam(
    image_bytes: bytes,
    target_class_idx: Optional[int] = None,
) -> str:
    """
    Generate a Grad-CAM heatmap for the given image.

    Args:
        image_bytes: Raw bytes of the uploaded image.
        target_class_idx: Class index to explain. If None, uses the top predicted class.

    Returns:
        Base64-encoded PNG string.
    """
    model = get_torch_model()
    target_layer = _get_target_layer(model)

    # Prepare input tensor with official transforms
    input_tensor = preprocess_image_tensor(image_bytes)  # (1, 3, H, W)

    # Determine target class
    if target_class_idx is None:
        with torch.no_grad():
            logits = model(input_tensor).cpu().numpy()[0]
        target_class_idx = int(np.argmax(softmax(logits)))

    # Build Grad-CAM targets
    from pytorch_grad_cam.utils.model_targets import ClassifierOutputTarget
    targets = [ClassifierOutputTarget(target_class_idx)]

    # Run Grad-CAM
    with GradCAM(model=model, target_layers=[target_layer]) as cam:
        grayscale_cam = cam(input_tensor=input_tensor, targets=targets)
        grayscale_cam = grayscale_cam[0]  # (H, W) float in [0, 1]

    # Resize original image to match tensor size (e.g. 300x300)
    H, W = grayscale_cam.shape
    orig_img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    orig_img_resized = orig_img.resize((W, H), Image.BILINEAR)
    rgb_img = np.array(orig_img_resized, dtype=np.float32) / 255.0  # (H, W, 3)

    # Blend heatmap onto original image
    visualization = show_cam_on_image(rgb_img, grayscale_cam, use_rgb=True, image_weight=0.5)
    vis_pil = Image.fromarray(visualization)

    # Encode to base64 PNG
    buf = io.BytesIO()
    vis_pil.save(buf, format="PNG")
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")
