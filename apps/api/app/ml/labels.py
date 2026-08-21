"""
ImageNet-1k class label mapping using timm's ImageNetInfo.
"""
from __future__ import annotations

import logging
from functools import lru_cache
from typing import Dict

logger = logging.getLogger(__name__)

_labels_dict: Dict[int, str] = {}


@lru_cache(maxsize=1)
def get_imagenet_labels() -> Dict[int, str]:
    """Return the full ImageNet-1k label mapping from timm ImageNetInfo."""
    global _labels_dict
    if not _labels_dict:
        try:
            from timm.data import ImageNetInfo
            info = ImageNetInfo()
            _labels_dict = {
                idx: info.index_to_description(idx).split(",")[0].strip()
                for idx in range(1000)
            }
        except Exception as exc:
            logger.warning(f"ImageNetInfo load failed ({exc}) — using fallback dictionary.")
            # Fallback to json if exists
            from pathlib import Path
            import json
            json_path = Path(__file__).parent / "imagenet_labels.json"
            if json_path.exists():
                with open(json_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                _labels_dict = {int(k): str(v).split(",")[0].strip() for k, v in data.items()}
    return _labels_dict
