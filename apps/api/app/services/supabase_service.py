"""
Supabase integration: store and retrieve predictions and batch jobs.

Uses the Supabase Python client with the service-role key for server-side
operations (bypasses RLS for write operations from the backend).
"""
from __future__ import annotations

import logging
from datetime import datetime
from functools import lru_cache
from typing import Any, Dict, List, Optional

from app.schemas.prediction import PredictionHistoryItem, TopKClass

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def _get_client():
    """Singleton Supabase client using the service-role key."""
    try:
        from supabase import create_client
        from app.config import get_settings

        s = get_settings()
        return create_client(s.supabase_url, s.supabase_service_role_key)
    except Exception as exc:
        logger.warning(f"Supabase client init failed (stub mode): {exc}")
        return None


async def insert_prediction(
    *,
    user_id: Optional[str],
    image_url: str,
    cloudinary_public_id: Optional[str],
    top_classes: List[TopKClass],
    heatmap_url: Optional[str] = None,
    batch_job_id: Optional[str] = None,
) -> Optional[str]:
    """
    Insert a prediction row into the Supabase predictions table.

    Returns the new prediction UUID, or None if Supabase is unavailable.
    """
    client = _get_client()
    if client is None:
        return None

    try:
        row = {
            "user_id": user_id,
            "image_url": image_url,
            "cloudinary_public_id": cloudinary_public_id,
            "top_classes": [tc.model_dump() for tc in top_classes],
            "heatmap_url": heatmap_url,
            "batch_job_id": batch_job_id,
        }
        response = client.table("predictions").insert(row).execute()
        data = response.data
        if data:
            return data[0].get("id")
    except Exception as exc:
        logger.error(f"Supabase insert_prediction error: {exc}")
    return None


async def get_prediction_history(
    user_id: str,
    page: int = 1,
    page_size: int = 20,
) -> tuple[List[PredictionHistoryItem], int]:
    """Return paginated prediction history for a user."""
    client = _get_client()
    if client is None:
        return [], 0

    try:
        offset = (page - 1) * page_size
        response = (
            client.table("predictions")
            .select("*", count="exact")
            .eq("user_id", user_id)
            .order("created_at", desc=True)
            .range(offset, offset + page_size - 1)
            .execute()
        )
        total = response.count or 0
        items = [
            PredictionHistoryItem(
                id=row["id"],
                image_url=row["image_url"],
                top_classes=[TopKClass(**tc) for tc in row["top_classes"]],
                heatmap_url=row.get("heatmap_url"),
                batch_job_id=row.get("batch_job_id"),
                created_at=row["created_at"],
            )
            for row in (response.data or [])
        ]
        return items, total
    except Exception as exc:
        logger.error(f"Supabase get_prediction_history error: {exc}")
        return [], 0


async def upsert_batch_job(
    job_id: str,
    user_id: Optional[str],
    status: str,
    total_images: int,
    completed_images: int,
) -> None:
    """Create or update a batch job row."""
    client = _get_client()
    if client is None:
        return
    try:
        client.table("batch_jobs").upsert({
            "id": job_id,
            "user_id": user_id,
            "status": status,
            "total_images": total_images,
            "completed_images": completed_images,
            "updated_at": datetime.utcnow().isoformat(),
        }).execute()
    except Exception as exc:
        logger.error(f"Supabase upsert_batch_job error: {exc}")
