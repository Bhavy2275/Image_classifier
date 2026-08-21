"""
Cloudinary integration: upload image bytes and return CDN URL.
Falls back to a base64 data URI when credentials are not configured.
"""
from __future__ import annotations

import base64
import io
import logging
from typing import Optional, Tuple

logger = logging.getLogger(__name__)


def _get_cloudinary():
    """Lazy import to avoid failure when credentials are absent."""
    import cloudinary
    import cloudinary.uploader
    from app.config import get_settings

    s = get_settings()
    if not s.cloudinary_api_key or "placeholder" in s.cloudinary_api_key or "your-" in s.cloudinary_api_key:
        raise ValueError("Cloudinary credentials not configured.")

    cloudinary.config(
        cloud_name=s.cloudinary_cloud_name,
        api_key=s.cloudinary_api_key,
        api_secret=s.cloudinary_api_secret,
        secure=True,
    )
    return cloudinary.uploader


def upload_image(
    image_bytes: bytes,
    filename: Optional[str] = None,
    folder: str = "visionai",
) -> Tuple[str, str]:
    """
    Upload image bytes to Cloudinary.
    Returns (secure_url, public_id) tuple.
    """
    try:
        uploader = _get_cloudinary()
        result = uploader.upload(
            io.BytesIO(image_bytes),
            folder=folder,
            public_id=filename,
            resource_type="image",
            overwrite=False,
            unique_filename=True,
        )
        return result["secure_url"], result["public_id"]
    except Exception as exc:
        logger.debug(f"Cloudinary upload fallback to data URI: {exc}")
        # Return base64 data URL so the image displays perfectly in local dev
        b64 = base64.b64encode(image_bytes).decode("utf-8")
        return f"data:image/jpeg;base64,{b64}", "local/data-uri"


def delete_image(public_id: str) -> None:
    """Delete an image from Cloudinary by its public_id."""
    try:
        uploader = _get_cloudinary()
        uploader.destroy(public_id)
    except Exception as exc:
        logger.warning(f"Cloudinary delete failed: {exc}")
