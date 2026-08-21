"""
Application configuration via pydantic-settings.
All values are read from environment variables (or .env file).
"""
from __future__ import annotations

from functools import lru_cache
from typing import List

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── CORS ────────────────────────────────────────────────
    cors_origins: str = "http://localhost:3000"

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: str) -> str:
        return v

    def get_cors_origins(self) -> List[str]:
        return [o.strip() for o in self.cors_origins.split(",")]

    # ── Supabase ────────────────────────────────────────────
    supabase_url: str = "https://placeholder.supabase.co"
    supabase_anon_key: str = "placeholder-anon-key"
    supabase_service_role_key: str = "placeholder-service-key"
    supabase_jwt_secret: str = "placeholder-jwt-secret"

    # ── Cloudinary ──────────────────────────────────────────
    cloudinary_cloud_name: str = "placeholder-cloud"
    cloudinary_api_key: str = "placeholder-api-key"
    cloudinary_api_secret: str = "placeholder-api-secret"
    cloudinary_upload_preset: str = "visionai_uploads"

    # ── Redis / RQ ──────────────────────────────────────────
    redis_url: str = "redis://localhost:6379/0"

    # ── ML Model ────────────────────────────────────────────
    onnx_model_path: str = "model_cache/efficientnet_b0.onnx"
    top_k: int = 5

    # ── App Meta ────────────────────────────────────────────
    app_name: str = "VisionAI"
    app_version: str = "0.1.0"
    debug: bool = False


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Cached settings singleton — avoids repeated env reads."""
    return Settings()
