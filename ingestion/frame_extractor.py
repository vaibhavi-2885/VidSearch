from pathlib import Path

import cv2
from PIL import Image

from ingestion.deduplicator import FrameDeduplicator
from ingestion.models import ExtractedFrame, VideoMetadata


class FrameExtractor:
    def __init__(self, output_root: Path, sample_rate: float, dedup_threshold: int) -> None:
        if sample_rate <= 0:
            raise ValueError("sample_rate must be greater than zero")

        self.output_root = output_root
        self.sample_rate = sample_rate
        self.dedup_threshold = dedup_threshold

    def extract(self, video: VideoMetadata) -> tuple[list[ExtractedFrame], int, int]:
        capture = cv2.VideoCapture(str(video.path))
        if not capture.isOpened():
            raise ValueError(f"Could not open video: {video.path}")

        video_frame_dir = self.output_root / video.video_id
        video_frame_dir.mkdir(parents=True, exist_ok=True)

        deduplicator = FrameDeduplicator(self.dedup_threshold)
        interval = max(1, round(video.fps / self.sample_rate)) if video.fps > 0 else 1
        extracted_count = 0
        skipped_duplicates = 0
        kept_frames: list[ExtractedFrame] = []

        frame_index = 0
        while True:
            ok, frame = capture.read()
            if not ok:
                break

            if frame_index % interval != 0:
                frame_index += 1
                continue

            extracted_count += 1
            timestamp_sec = frame_index / video.fps if video.fps > 0 else float(extracted_count - 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(rgb_frame)
            keep, frame_hash = deduplicator.should_keep(image)

            if not keep:
                skipped_duplicates += 1
                frame_index += 1
                continue

            frame_path = video_frame_dir / f"{int(round(timestamp_sec)):06d}.jpg"
            image.save(frame_path, format="JPEG", quality=90)
            kept_frames.append(
                ExtractedFrame(
                    video_id=video.video_id,
                    timestamp_sec=round(timestamp_sec, 3),
                    frame_index=frame_index,
                    path=frame_path,
                    image_hash=frame_hash,
                )
            )
            frame_index += 1

        capture.release()
        return kept_frames, extracted_count, skipped_duplicates
