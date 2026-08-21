"""
Redis / RQ queue setup for async batch inference jobs.
"""
from __future__ import annotations

import logging
from functools import lru_cache
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

QUEUE_NAME = "visionai-batch"


@lru_cache(maxsize=1)
def get_redis_connection():
    """Return a cached Redis connection."""
    try:
        import redis
        from app.config import get_settings

        s = get_settings()
        conn = redis.from_url(s.redis_url, decode_responses=False)
        conn.ping()  # fail fast if Redis is unreachable
        return conn
    except Exception as exc:
        logger.warning(f"Redis connection failed (stub mode): {exc}")
        return None


@lru_cache(maxsize=1)
def get_queue():
    """Return a cached RQ Queue."""
    try:
        from rq import Queue

        conn = get_redis_connection()
        if conn is None:
            return None
        return Queue(QUEUE_NAME, connection=conn)
    except Exception as exc:
        logger.warning(f"RQ Queue init failed: {exc}")
        return None


def enqueue_batch_image(
    job_id: str,
    image_bytes: bytes,
    filename: str,
    user_id: Optional[str],
    image_index: int,
) -> Optional[str]:
    """
    Enqueue a single image for batch inference.

    Returns the RQ job ID, or None if queue is unavailable.
    """
    queue = get_queue()
    if queue is None:
        logger.warning("Queue unavailable — batch image will not be processed.")
        return None

    from app.workers.batch_worker import process_batch_image

    job = queue.enqueue(
        process_batch_image,
        args=(job_id, image_bytes, filename, user_id, image_index),
        job_timeout=120,        # 2 min per image max
        result_ttl=3600,        # keep result for 1 hour
        failure_ttl=3600,
    )
    return job.id


def get_job_status(rq_job_id: str) -> Dict[str, Any]:
    """Return the status dict for a single RQ job."""
    conn = get_redis_connection()
    if conn is None:
        return {"status": "unavailable"}

    try:
        from rq.job import Job

        job = Job.fetch(rq_job_id, connection=conn)
        return {
            "status": job.get_status().value,
            "result": job.result,
            "exc_info": job.exc_info,
        }
    except Exception as exc:
        logger.error(f"get_job_status error: {exc}")
        return {"status": "unknown"}
