"""
Tests for the POST /predict endpoint.
"""
from __future__ import annotations

import io


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "VisionAI"


def test_predict_returns_top5(client, dummy_image_bytes):
    """A valid JPEG upload should return 5 predictions."""
    response = client.post(
        "/predict",
        files={"image": ("test.jpg", io.BytesIO(dummy_image_bytes), "image/jpeg")},
        data={"include_heatmap": "false"},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert "top_classes" in data
    assert len(data["top_classes"]) == 5

    first = data["top_classes"][0]
    assert first["rank"] == 1
    assert "label" in first
    assert 0.0 <= first["confidence"] <= 1.0


def test_predict_includes_heatmap(client, dummy_image_bytes):
    """When include_heatmap=true, the response should contain heatmap_base64."""
    response = client.post(
        "/predict",
        files={"image": ("test.jpg", io.BytesIO(dummy_image_bytes), "image/jpeg")},
        data={"include_heatmap": "true"},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["heatmap_base64"] is not None
    assert len(data["heatmap_base64"]) > 0


def test_predict_includes_image_url(client, dummy_image_bytes):
    """The response should include the Cloudinary CDN URL."""
    response = client.post(
        "/predict",
        files={"image": ("test.jpg", io.BytesIO(dummy_image_bytes), "image/jpeg")},
        data={"include_heatmap": "false"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["image_url"].startswith("http")


def test_predict_invalid_content_type(client, dummy_image_bytes):
    """Uploading a non-image file should return 415."""
    response = client.post(
        "/predict",
        files={"image": ("test.pdf", io.BytesIO(b"pdf content"), "application/pdf")},
        data={"include_heatmap": "false"},
    )
    assert response.status_code == 415


def test_predict_processing_time_present(client, dummy_image_bytes):
    """Response should include processing time in milliseconds."""
    response = client.post(
        "/predict",
        files={"image": ("test.jpg", io.BytesIO(dummy_image_bytes), "image/jpeg")},
        data={"include_heatmap": "false"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "processing_time_ms" in data
    assert isinstance(data["processing_time_ms"], float)
    assert data["processing_time_ms"] >= 0
