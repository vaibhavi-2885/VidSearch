from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "VidSearch"
    env: str = "development"
    api_host: str = "127.0.0.1"
    api_port: int = 8000
    frontend_port: int = 8501
    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    qdrant_collection: str = "video_frames"
    redis_url: str = "redis://localhost:6379/0"
    database_url: str = "sqlite:///./data/app.db"
    upload_dir: Path = Path("./data/uploads")
    frame_dir: Path = Path("./data/frames")
    temp_dir: Path = Path("./data/temp")
    frame_sample_rate: float = 1.0
    dedup_hash_threshold: int = 5
    clip_model: str = "openai/clip-vit-base-patch32"
    batch_size: int = 32

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
