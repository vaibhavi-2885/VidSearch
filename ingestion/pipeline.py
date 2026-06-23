import json
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
        result = IngestionResult(
            video=video,
            frames=frames,
            extracted_count=extracted_count,
            kept_count=len(frames),
            skipped_duplicates=skipped_duplicates,
        )
        manifest_path = self._save_manifest(result)
        return IngestionResult(
            video=video,
            frames=frames,
            extracted_count=extracted_count,
            kept_count=len(frames),
            skipped_duplicates=skipped_duplicates,
            manifest_path=manifest_path,
        )

    def _save_manifest(self, result: IngestionResult) -> Path:
        manifest_dir = self.extractor.output_root / result.video.video_id
        manifest_dir.mkdir(parents=True, exist_ok=True)
        manifest_path = manifest_dir / "metadata.json"

        with manifest_path.open("w", encoding="utf-8") as handle:
            json.dump(result.to_dict(), handle, indent=2)

        return manifest_path
