"""
Batch upload endpoints.

POST /batch/predict  — Accept multiple images, enqueue RQ jobs, return job_id
GET  /batch/status/{job_id} — Poll overall batch status + per-image results
"""
from __future__ import annotations

import json
import logging
import uuid
from typing import List, Optional

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from app.routers.auth import get_current_user
from app.schemas.batch import BatchJobResponse, BatchJobStatus, BatchStatusResponse, BatchJobItem
from app.services import queue_service, supabase_service

logger = logging.getLogger(__name__)
router = APIRouter()

_MAX_BATCH_SIZE = 20
_ALLOWED_MIME = {"image/jpeg", "image/png", "image/webp"}

# In-memory job store (fallback when Redis unavailable). In production this
# is persisted to Redis so it survives worker restarts.
_job_store: dict = {}


@router.post("/predict", response_model=BatchJobResponse)
async def batch_predict(
    images: List[UploadFile] = File(..., description="List of images to classify"),
    user: Optional[dict] = Depends(get_current_user),
):
    """
    Submit multiple images for async batch inference.

    Each image is enqueued as an independent RQ job.
    Returns a job_id to poll with GET /batch/status/{job_id}.
    """
    if not images:
        raise HTTPException(status_code=400, detail="No images provided.")
    if len(images) > _MAX_BATCH_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"Maximum {_MAX_BATCH_SIZE} images per batch.",
        )

    job_id = str(uuid.uuid4())
    user_id = user.get("sub") if user else None

    items = []
    rq_job_ids = []

    for idx, upload in enumerate(images):
        if upload.content_type not in _ALLOWED_MIME:
            items.append(BatchJobItem(
                filename=upload.filename or f"image_{idx}",
                status=BatchJobStatus.FAILED,
                error=f"Unsupported file type: {upload.content_type}",
            ))
            continue

        image_bytes = await upload.read()
        rq_id = queue_service.enqueue_batch_image(
            job_id=job_id,
            image_bytes=image_bytes,
            filename=upload.filename or f"image_{idx}.jpg",
            user_id=user_id,
            image_index=idx,
        )
        rq_job_ids.append(rq_id)
        items.append(BatchJobItem(
            filename=upload.filename or f"image_{idx}",
            status=BatchJobStatus.PENDING,
        ))

    # Persist job metadata to in-memory store + Supabase
    _job_store[job_id] = {
        "status": BatchJobStatus.PENDING,
        "total_images": len(images),
        "completed_images": 0,
        "rq_job_ids": rq_job_ids,
        "items": [item.model_dump() for item in items],
        "user_id": user_id,
    }

    await supabase_service.upsert_batch_job(
        job_id=job_id,
        user_id=user_id,
        status=BatchJobStatus.PENDING,
        total_images=len(images),
        completed_images=0,
    )

    return BatchJobResponse(
        job_id=job_id,
        total_images=len(images),
        status=BatchJobStatus.PENDING,
    )


@router.get("/status/{job_id}", response_model=BatchStatusResponse)
async def batch_status(
    job_id: str,
    user: Optional[dict] = Depends(get_current_user),
):
    """
    Poll the status of a batch inference job.

    Aggregates per-image RQ job results and returns overall + per-image status.
    """
    job_data = _job_store.get(job_id)
    if job_data is None:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found.")

    rq_job_ids = job_data.get("rq_job_ids", [])
    items = [BatchJobItem(**item) for item in job_data["items"]]
    completed = 0

    for i, rq_id in enumerate(rq_job_ids):
        if rq_id is None:
            continue
        job_status_data = queue_service.get_job_status(rq_id)
        rq_status = job_status_data.get("status", "unknown")
        result = job_status_data.get("result")

        if rq_status == "finished" and result:
            items[i] = BatchJobItem(**result)
            completed += 1
        elif rq_status == "failed":
            items[i].status = BatchJobStatus.FAILED
            items[i].error = str(job_status_data.get("exc_info", "Unknown error"))
            completed += 1
        elif rq_status in ("started", "deferred"):
            items[i].status = BatchJobStatus.PROCESSING

    job_data["completed_images"] = completed
    total = job_data["total_images"]

    if completed >= total:
        overall_status = BatchJobStatus.COMPLETED
    elif completed > 0:
        overall_status = BatchJobStatus.PROCESSING
    else:
        overall_status = BatchJobStatus.PENDING

    job_data["status"] = overall_status

    return BatchStatusResponse(
        job_id=job_id,
        status=overall_status,
        total_images=total,
        completed_images=completed,
        items=items,
    )
