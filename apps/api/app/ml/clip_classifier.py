"""
OpenCLIP zero-shot image classifier with open-vocabulary label set.

Features:
- Fast vectorized prompt encoding
- Local disk caching of text features (.pt) for instant startup
- Comprehensive label set covering gaming consoles, modern electronics,
  household objects, food, vehicles, tools, clothing, animals, and ImageNet.
"""
from __future__ import annotations

import io
import logging
from functools import lru_cache
from pathlib import Path
from typing import List, Tuple

import open_clip
import torch
from PIL import Image

logger = logging.getLogger(__name__)

_CLIP_MODEL_NAME = "ViT-B-32"
_CLIP_PRETRAINED = "laion2b_s34b_b79k"
_CACHE_PATH = Path(__file__).parent / "clip_embeddings_cache.pt"


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
    """
    from app.ml.labels import get_imagenet_labels
    from app.ml.extended_labels import EXTENDED_LABELS

    imagenet = get_imagenet_labels()
    imagenet_names = [imagenet.get(i, f"class {i}").split(",")[0].strip() for i in range(1000)]

    seen = set()
    merged = []
    # Put extended modern labels first so specific matches take natural priority
    for label in list(EXTENDED_LABELS) + imagenet_names:
        key = label.lower()
        if key not in seen:
            seen.add(key)
            merged.append(label)

    logger.info(f"Total CLIP candidate classes: {len(merged)}")
    return merged


_TEMPLATES = [
    "a photo of a {}.",
    "a photo of the {}.",
    "a close-up photo of a {}.",
    "a rendering of a {}.",
    "a 3d render of a {}.",
    "a clean photo of a {}.",
    "a photo of many {}.",
    "{}.",
]


def _get_text_features() -> Tuple[torch.Tensor, List[str]]:
    """
    Load or compute normalized text embeddings for all candidate labels.
    Uses disk caching to guarantee instant (<5ms) retrieval on subsequent runs.
    """
    all_labels = _build_all_labels()

    if _CACHE_PATH.exists():
        try:
            cached = torch.load(str(_CACHE_PATH), weights_only=True)
            if cached.get("labels") == all_labels:
                return cached["features"], all_labels
        except Exception as exc:
            logger.warning(f"Failed to load cached embeddings ({exc}), recomputing...")

    model, _, tokenizer = _load_clip()
    logger.info(f"Fast encoding {len(all_labels)} text prompts for zero-shot classification...")

    # Fast vectorized batch encoding
    prompts = [f"a photo of a {label}" for label in all_labels]
    batch_size = 256
    all_embeddings = []

    with torch.no_grad():
        for i in range(0, len(prompts), batch_size):
            batch = prompts[i : i + batch_size]
            tokens = tokenizer(batch)
            emb = model.encode_text(tokens)
            emb = emb / emb.norm(dim=-1, keepdim=True)
            all_embeddings.append(emb)

        text_features = torch.cat(all_embeddings, dim=0)

    try:
        torch.save({"features": text_features, "labels": all_labels}, str(_CACHE_PATH))
        logger.info(f"Saved text embeddings cache to {_CACHE_PATH}")
    except Exception as exc:
        logger.warning(f"Could not persist embeddings cache: {exc}")

    return text_features, all_labels


def clip_classify(image_bytes: bytes, top_k: int = 5) -> List[Tuple[int, str, float]]:
    """
    Classify an image using OpenCLIP zero-shot against open-vocabulary labels.

    Returns list of (class_index, label, confidence) tuples sorted by confidence.
    """
    model, preprocess, _ = _load_clip()
    text_features, all_labels = _get_text_features()

    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image_tensor = preprocess(img).unsqueeze(0)

    with torch.no_grad():
        image_features = model.encode_image(image_tensor)
        image_features = image_features / image_features.norm(dim=-1, keepdim=True)
        # Cosine similarity scaled by 100
        logits = (100.0 * image_features @ text_features.T).softmax(dim=-1)[0]

    top_probs, top_positions = logits.topk(top_k)

    results = []
    for prob, pos in zip(top_probs, top_positions):
        idx = pos.item()
        label = all_labels[idx]
        results.append((idx, label, float(prob.item())))

    return results
