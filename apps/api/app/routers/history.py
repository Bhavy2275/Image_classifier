"""
Prediction history endpoint.

GET /history — Returns paginated prediction history for the authenticated user.
"""
from __future__ import annotations

from fastapi import APIRouter, Depends, Query

from app.routers.auth import require_current_user
from app.schemas.prediction import HistoryResponse
from app.services import supabase_service

router = APIRouter()


@router.get("", response_model=HistoryResponse)
async def get_history(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    user: dict = Depends(require_current_user),
):
    """
    Return paginated prediction history for the authenticated user.
    Results are sorted newest-first.
    """
    user_id = user.get("sub", "")
    items, total = await supabase_service.get_prediction_history(
        user_id=user_id,
        page=page,
        page_size=page_size,
    )

    return HistoryResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
    )
