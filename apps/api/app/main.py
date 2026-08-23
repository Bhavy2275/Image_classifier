"""
FastAPI application entrypoint.
"""
from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.ml.model import get_model_session, get_torch_model
from app.routers import auth, batch, history, predict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Warm up ML models on startup so first request is fast."""
    logger.info("🔥 Warming up OpenCLIP zero-shot classifier …")
    try:
        from app.ml.clip_classifier import _load_clip, _get_text_features
        _load_clip()
        _get_text_features()   # pre-encode candidate text prompts
        logger.info("✅ CLIP ready.")
    except Exception as exc:
        logger.warning(f"CLIP warmup failed ({exc}), will use EfficientNetV2-S fallback.")
        get_model_session()
        get_torch_model()
    logger.info("🔥 Warming up EfficientNetV2-S for Grad-CAM …")
    get_torch_model()    # always load for Grad-CAM heatmaps
    logger.info("✅ All models ready.")
    yield
    logger.info("👋 Shutting down VisionAI API.")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Full-stack image classification SaaS with explainable AI.",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# ── CORS ────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ─────────────────────────────────────────────────
app.include_router(predict.router, tags=["Inference"])
app.include_router(batch.router, prefix="/batch", tags=["Batch"])
app.include_router(history.router, prefix="/history", tags=["History"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])


@app.get("/health", tags=["Health"])
async def health_check() -> dict:
    return {
        "status": "ok",
        "service": settings.app_name,
        "version": settings.app_version,
    }
