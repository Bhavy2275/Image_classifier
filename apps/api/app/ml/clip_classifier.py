"""
OpenCLIP zero-shot image classifier with open-vocabulary label set.

Uses ViT-B-32 trained on LAION-2B for zero-shot classification.
Scores the image against natural-language prompts combining:
  1. All 1000 ImageNet classes (animals, objects, scenes)
  2. Extended labels covering modern electronics, gaming, food, brands, etc.

This means it can correctly identify a PlayStation 5, iPhone, pizza, etc.
"""
from __future__ import annotations

import io
import logging
from functools import lru_cache
from typing import List, Tuple

import open_clip
import torch
from PIL import Image

logger = logging.getLogger(__name__)

_CLIP_MODEL_NAME = "ViT-B-32"
_CLIP_PRETRAINED = "laion2b_s34b_b79k"


@lru_cache(maxsize=1)
def _load_clip():
    """Load and cache the CLIP model, preprocessor, and tokenizer."""
    logger.info(f"Loading OpenCLIP {_CLIP_MODEL_NAME} ({_CLIP_PRETRAINED})...")
    model, _, preprocess = open_clip.create_model_and_transforms(
        _CLIP_MODEL_NAME, pretrained=_CLIP_PRETRAINED
    )
    tokenizer = open_clip.get_tokenizer(_CLIP_MODEL_NAME)
    model.eval()
    logger.info("OpenCLIP ready.")
    return model, preprocess, tokenizer


@lru_cache(maxsize=1)
def _build_all_labels() -> List[str]:
    """
    Build merged label list: ImageNet 1000 + extended open-vocabulary labels.
    Returns a flat list of unique label strings.
    """
    from app.ml.labels import get_imagenet_labels
    from app.ml.extended_labels import EXTENDED_LABELS

    imagenet = get_imagenet_labels()
    # Take the first name from comma-separated ImageNet labels
    imagenet_names = [imagenet.get(i, f"class {i}").split(",")[0].strip() for i in range(1000)]

    # Merge, deduplicate preserving order (ImageNet first, then extended)
    seen = set()
    merged = []
    for label in imagenet_names + list(EXTENDED_LABELS):
        key = label.lower()
        if key not in seen:
            seen.add(key)
            merged.append(label)

    logger.info(f"Total CLIP label candidates: {len(merged)}")
    return merged


@lru_cache(maxsize=1)
def _get_text_features() -> Tuple[torch.Tensor, List[str]]:
    """
    Pre-compute and cache text embeddings for all labels.
    Uses ensemble of prompt templates for better zero-shot accuracy.
    """
    model, _, tokenizer = _load_clip()
    all_labels = _build_all_labels()

    # Ensemble templates (CLIP paper shows this improves accuracy by ~3-5%)
    templates = [
        "a photo of a {}",
        "a photo of the {}",
        "a picture of a {}",
        "an image of a {}",
        "{}",
    ]

    logger.info(f"Encoding {len(all_labels)} labels with {len(templates)} templates each...")

    all_text_features = []
    for template in templates:
        prompts = [template.format(label) for label in all_labels]
        # Encode in batches to avoid OOM
        batch_size = 256
        features_list = []
        for i in range(0, len(prompts), batch_size):
            batch = prompts[i : i + batch_size]
            tokens = tokenizer(batch)
            with torch.no_grad():
                feats = model.encode_text(tokens)
                feats = feats / feats.norm(dim=-1, keepdim=True)
            features_list.append(feats)
        all_text_features.append(torch.cat(features_list, dim=0))

    # Average across templates (ensemble)
    text_features = torch.stack(all_text_features).mean(dim=0)
    text_features = text_features / text_features.norm(dim=-1, keepdim=True)

    logger.info("CLIP text embeddings cached.")
    return text_features, all_labels


def clip_classify(image_bytes: bytes, top_k: int = 5) -> List[Tuple[int, str, float]]:
    """
    Classify an image using OpenCLIP zero-shot against open-vocabulary labels.

    Returns list of (class_index, label, confidence) tuples sorted by confidence.
    class_index is the position in the merged label list (0-based).
    """
    model, preprocess, _ = _load_clip()
    text_features, all_labels = _get_text_features()

    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image_tensor = preprocess(img).unsqueeze(0)

    with torch.no_grad():
        image_features = model.encode_image(image_tensor)
        image_features = image_features / image_features.norm(dim=-1, keepdim=True)
        logits = (100.0 * image_features @ text_features.T).softmax(dim=-1)[0]

    top_probs, top_positions = logits.topk(top_k)

    results = []
    for prob, pos in zip(top_probs, top_positions):
        idx = pos.item()
        label = all_labels[idx]
        results.append((idx, label, float(prob.item())))

    return results
