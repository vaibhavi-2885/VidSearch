from pathlib import Path

from ingestion.frame_extractor import FrameExtractor
from ingestion.models import IngestionResult
from ingestion.video_reader import VideoReader


class IngestionPipeline:
    def __init__(self, frame_dir: Path, sample_rate: float, dedup_threshold: int) -> None:
        self.reader = VideoReader()
        self.extractor = FrameExtractor(frame_dir, sample_rate, dedup_threshold)

    def process(self, video_path: Path) -> IngestionResult:
        video = self.reader.read_metadata(video_path)
        frames, extracted_count, skipped_duplicates = self.extractor.extract(video)
        return IngestionResult(
            video=video,
            frames=frames,
            extracted_count=extracted_count,
            kept_count=len(frames),
            skipped_duplicates=skipped_duplicates,
        )
