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
    """Warm up ML models in background so server starts and serves /health immediately."""
    import asyncio

    async def _warmup() -> None:
        logger.info("🔥 Starting background warmup for ML models...")
        try:
            from app.ml.clip_classifier import _load_clip, _get_text_features
            _load_clip()
            _get_text_features()
            logger.info("✅ OpenCLIP classifier ready.")
        except Exception as exc:
            logger.warning(f"CLIP warmup error ({exc}), will use fallback.")
        try:
            get_torch_model()
            logger.info("✅ Grad-CAM PyTorch model ready.")
        except Exception as exc:
            logger.warning(f"PyTorch model warmup error ({exc})")

    # Start background task without blocking the HTTP server startup
    asyncio.create_task(_warmup())
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

# ── CORS (Allow all origins for seamless Vercel/localhost integration) ─────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_origin_regex=r".*",
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


if __name__ == "__main__":
    import os
    import uvicorn

    port = int(os.environ.get("PORT", os.environ.get("API_PORT", 8000)))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port)

