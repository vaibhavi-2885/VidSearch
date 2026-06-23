from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from api.config import Settings, get_settings
from ingestion.pipeline import IngestionPipeline
from storage.local_storage import LocalStorage

router = APIRouter(prefix="/videos", tags=["videos"])

ALLOWED_VIDEO_EXTENSIONS = {".mp4", ".mov", ".avi", ".mkv"}


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_video(
    video: UploadFile = File(...),
    settings: Settings = Depends(get_settings),
) -> dict:
    extension = Path(video.filename or "").suffix.lower()
    if extension not in ALLOWED_VIDEO_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported video format",
        )

    storage = LocalStorage(settings.upload_dir, settings.frame_dir)
    saved_video = await storage.save_upload(video)

    pipeline = IngestionPipeline(
        frame_dir=settings.frame_dir,
        sample_rate=settings.frame_sample_rate,
        dedup_threshold=settings.dedup_hash_threshold,
    )
    result = pipeline.process(saved_video)
    return result.to_dict()
