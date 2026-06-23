from pathlib import Path
from uuid import uuid4

import cv2

from ingestion.models import VideoMetadata


class VideoReader:
    def read_metadata(self, video_path: Path) -> VideoMetadata:
        capture = cv2.VideoCapture(str(video_path))
        if not capture.isOpened():
            raise ValueError(f"Could not open video: {video_path}")

        fps = float(capture.get(cv2.CAP_PROP_FPS) or 0)
        frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
        width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH) or 0)
        height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT) or 0)
        capture.release()

        duration_sec = frame_count / fps if fps > 0 else 0.0

        return VideoMetadata(
            video_id=video_path.stem.split("_", 1)[0] or str(uuid4()),
            filename=video_path.name,
            path=video_path,
            duration_sec=round(duration_sec, 3),
            fps=round(fps, 3),
            frame_count=frame_count,
            width=width,
            height=height,
        )
