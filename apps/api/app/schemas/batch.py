"""
Pydantic v2 schemas for batch job request/response models.
"""
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field

from app.schemas.prediction import TopKClass


class BatchJobStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class BatchJobItem(BaseModel):
    """Status of a single image within a batch job."""
    filename: str
    status: BatchJobStatus
    prediction_id: Optional[str] = None
    image_url: Optional[str] = None
    top_classes: Optional[List[TopKClass]] = None
    heatmap_base64: Optional[str] = None
    error: Optional[str] = None


class BatchJobResponse(BaseModel):
    """Response from POST /batch/predict (job submission)."""
    job_id: str
    total_images: int
    status: BatchJobStatus = BatchJobStatus.PENDING
    message: str = "Batch job queued successfully."


class BatchStatusResponse(BaseModel):
    """Response from GET /batch/status/{job_id}."""
    job_id: str
    status: BatchJobStatus
    total_images: int
    completed_images: int
    items: List[BatchJobItem]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
