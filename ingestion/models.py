from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class VideoMetadata:
    video_id: str
    filename: str
    path: Path
    duration_sec: float
    fps: float
    frame_count: int
    width: int
    height: int

    def to_dict(self) -> dict:
        data = asdict(self)
        data["path"] = str(self.path)
        return data


@dataclass(frozen=True)
class ExtractedFrame:
    video_id: str
    timestamp_sec: float
    frame_index: int
    path: Path
    image_hash: str

    def to_dict(self) -> dict:
        data = asdict(self)
        data["path"] = str(self.path)
        return data


@dataclass(frozen=True)
class IngestionResult:
    video: VideoMetadata
    frames: list[ExtractedFrame]
    extracted_count: int
    kept_count: int
    skipped_duplicates: int

    def to_dict(self) -> dict:
        return {
            "video": self.video.to_dict(),
            "frames": [frame.to_dict() for frame in self.frames],
            "summary": {
                "extracted_count": self.extracted_count,
                "kept_count": self.kept_count,
                "skipped_duplicates": self.skipped_duplicates,
            },
        }
