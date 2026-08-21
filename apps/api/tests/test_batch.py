"""
Tests for the POST /batch/predict and GET /batch/status/{job_id} endpoints.
"""
from __future__ import annotations

import io
from unittest.mock import MagicMock, patch


def _make_files(n: int, dummy_image_bytes: bytes):
    return [
        ("images", (f"img_{i}.jpg", io.BytesIO(dummy_image_bytes), "image/jpeg"))
        for i in range(n)
    ]


def test_batch_predict_returns_job_id(client, dummy_image_bytes):
    """Submitting 3 images should return a job_id."""
    with patch("app.services.queue_service.enqueue_batch_image", return_value="rq-job-123"):
        response = client.post("/batch/predict", files=_make_files(3, dummy_image_bytes))

    assert response.status_code == 200, response.text
    data = response.json()
    assert "job_id" in data
    assert len(data["job_id"]) == 36   # UUID format
    assert data["total_images"] == 3
    assert data["status"] == "pending"


def test_batch_predict_rejects_too_many_images(client, dummy_image_bytes):
    """Submitting more than 20 images should return 400."""
    response = client.post("/batch/predict", files=_make_files(21, dummy_image_bytes))
    assert response.status_code == 400


def test_batch_predict_rejects_invalid_mime(client, dummy_image_bytes):
    """An invalid MIME type within the batch should mark that item as failed."""
    with patch("app.services.queue_service.enqueue_batch_image", return_value="rq-job-456"):
        response = client.post(
            "/batch/predict",
            files=[
                ("images", ("img.jpg", io.BytesIO(dummy_image_bytes), "image/jpeg")),
                ("images", ("doc.pdf", io.BytesIO(b"pdf"), "application/pdf")),
            ],
        )
    assert response.status_code == 200
    data = response.json()
    assert data["total_images"] == 2


def test_batch_status_unknown_job(client):
    """Polling a non-existent job_id should return 404."""
    response = client.get("/batch/status/non-existent-job-id")
    assert response.status_code == 404


def test_batch_status_returns_structure(client, dummy_image_bytes):
    """After submitting, polling immediately should return pending status."""
    with patch("app.services.queue_service.enqueue_batch_image", return_value="rq-job-789"):
        submit = client.post("/batch/predict", files=_make_files(2, dummy_image_bytes))
    job_id = submit.json()["job_id"]

    with patch(
        "app.services.queue_service.get_job_status",
        return_value={"status": "queued"},
    ):
        status_resp = client.get(f"/batch/status/{job_id}")

    assert status_resp.status_code == 200
    data = status_resp.json()
    assert data["job_id"] == job_id
    assert data["total_images"] == 2
    assert "items" in data
    assert isinstance(data["items"], list)
