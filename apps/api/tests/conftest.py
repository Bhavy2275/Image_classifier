"""
Shared pytest fixtures for the VisionAI API test suite.
"""
from __future__ import annotations

import io
import os
from typing import Generator
from unittest.mock import MagicMock, patch

import numpy as np
import pytest
from fastapi.testclient import TestClient
from PIL import Image

# Set environment variables BEFORE importing app modules
os.environ.setdefault("SUPABASE_URL", "https://mock.supabase.co")
os.environ.setdefault("SUPABASE_ANON_KEY", "mock-anon-key")
os.environ.setdefault("SUPABASE_SERVICE_ROLE_KEY", "mock-service-key")
os.environ.setdefault("SUPABASE_JWT_SECRET", "mock-jwt-secret")
os.environ.setdefault("CLOUDINARY_CLOUD_NAME", "mock-cloud")
os.environ.setdefault("CLOUDINARY_API_KEY", "mock-api-key")
os.environ.setdefault("CLOUDINARY_API_SECRET", "mock-secret")
os.environ.setdefault("REDIS_URL", "redis://localhost:6379/0")
os.environ.setdefault("ONNX_MODEL_PATH", "model_cache/test.onnx")


def _make_dummy_image_bytes(width: int = 64, height: int = 64) -> bytes:
    """Return JPEG bytes for a random test image."""
    img = Image.fromarray(
        np.random.randint(0, 255, (height, width, 3), dtype=np.uint8)
    )
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()


@pytest.fixture
def dummy_image_bytes() -> bytes:
    return _make_dummy_image_bytes()


@pytest.fixture
def mock_onnx_session():
    """Mock ONNX Runtime InferenceSession that returns random logits."""
    session = MagicMock()
    # get_inputs()[0].name -> "input"
    mock_input = MagicMock()
    mock_input.name = "input"
    session.get_inputs.return_value = [mock_input]
    # run() returns random (1, 1000) logits
    session.run.return_value = [np.random.randn(1, 1000).astype(np.float32)]
    return session


@pytest.fixture
def client(mock_onnx_session) -> Generator:
    """FastAPI TestClient with ONNX session and external services mocked."""
    with (
        patch("app.ml.model.get_model_session", return_value=mock_onnx_session),
        patch("app.ml.model.get_torch_model", return_value=MagicMock()),
        patch("app.ml.gradcam.generate_gradcam", return_value="base64heatmap=="),
        patch(
            "app.services.cloudinary_service.upload_image",
            return_value=("https://mock.cdn/image.jpg", "visionai/mock"),
        ),
        patch(
            "app.services.supabase_service.insert_prediction",
            return_value="mock-prediction-id",
        ),
        patch(
            "app.services.supabase_service.upsert_batch_job",
            return_value=None,
        ),
    ):
        from app.main import app
        with TestClient(app) as c:
            yield c
