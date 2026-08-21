"""
Pydantic v2 schemas for prediction request/response models.
"""
from __future__ import annotations

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class TopKClass(BaseModel):
    """A single predicted class with its rank and confidence."""
    rank: int = Field(..., ge=1, description="Rank (1 = top prediction)")
    class_index: int = Field(..., ge=0, lt=1000)
    label: str
    confidence: float = Field(..., ge=0.0, le=1.0)


class PredictionResult(BaseModel):
    """Full response from /predict."""
    prediction_id: Optional[str] = None
    image_url: str
    top_classes: List[TopKClass]
    heatmap_base64: Optional[str] = Field(
        None,
        description="Base64-encoded PNG of the Grad-CAM heatmap overlaid on the image.",
    )
    processing_time_ms: float
    created_at: datetime = Field(default_factory=datetime.utcnow)


class PredictionHistoryItem(BaseModel):
    """Row returned from Supabase predictions table."""
    id: str
    image_url: str
    top_classes: List[TopKClass]
    heatmap_url: Optional[str] = None
    batch_job_id: Optional[str] = None
    created_at: datetime


class HistoryResponse(BaseModel):
    items: List[PredictionHistoryItem]
    total: int
    page: int
    page_size: int
