"""
Redis / RQ queue setup for async batch inference jobs.
"""
from __future__ import annotations

import logging
import uuid
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

QUEUE_NAME = "visionai-batch"

_thread_pool = ThreadPoolExecutor(max_workers=4)
_in_memory_jobs: Dict[str, Dict[str, Any]] = {}


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
        logger.warning(f"Redis connection failed (using in-memory background worker): {exc}")
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

    Uses Redis/RQ if available, or falls back to in-memory ThreadPoolExecutor.
    """
    queue = get_queue()
    if queue is not None:
        try:
            from app.workers.batch_worker import process_batch_image

            job = queue.enqueue(
                process_batch_image,
                args=(job_id, image_bytes, filename, user_id, image_index),
                job_timeout=120,        # 2 min per image max
                result_ttl=3600,        # keep result for 1 hour
                failure_ttl=3600,
            )
            return job.id
        except Exception as exc:
            logger.warning(f"Failed to enqueue to RQ ({exc}), falling back to in-memory worker.")

    # In-memory ThreadPoolExecutor fallback
    mem_job_id = f"mem_{uuid.uuid4()}"
    _in_memory_jobs[mem_job_id] = {"status": "started", "result": None, "exc_info": None}

    def _run_task():
        from app.workers.batch_worker import process_batch_image
        try:
            result = process_batch_image(
                job_id=job_id,
                image_bytes=image_bytes,
                filename=filename,
                user_id=user_id,
                image_index=image_index,
            )
            _in_memory_jobs[mem_job_id] = {
                "status": "finished",
                "result": result,
                "exc_info": None,
            }
        except Exception as exc:
            logger.error(f"In-memory worker error for {filename}: {exc}", exc_info=True)
            _in_memory_jobs[mem_job_id] = {
                "status": "failed",
                "result": None,
                "exc_info": str(exc),
            }

    _thread_pool.submit(_run_task)
    return mem_job_id


def get_job_status(rq_job_id: str) -> Dict[str, Any]:
    """Return the status dict for a single RQ or in-memory job."""
    if rq_job_id.startswith("mem_") or rq_job_id in _in_memory_jobs:
        return _in_memory_jobs.get(rq_job_id, {"status": "unknown"})

    conn = get_redis_connection()
    if conn is None:
        return _in_memory_jobs.get(rq_job_id, {"status": "unavailable"})

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
        return _in_memory_jobs.get(rq_job_id, {"status": "unknown"})

