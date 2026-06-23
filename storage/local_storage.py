from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile


class LocalStorage:
    def __init__(self, upload_dir: Path, frame_dir: Path) -> None:
        self.upload_dir = upload_dir
        self.frame_dir = frame_dir
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        self.frame_dir.mkdir(parents=True, exist_ok=True)

    async def save_upload(self, upload: UploadFile) -> Path:
        extension = Path(upload.filename or "").suffix.lower()
        filename = f"{uuid4().hex}{extension}"
        destination = self.upload_dir / filename

        with destination.open("wb") as target:
            while chunk := await upload.read(1024 * 1024):
                target.write(chunk)

        await upload.close()
        return destination
