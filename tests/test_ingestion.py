from pathlib import Path

import cv2
import numpy as np

from ingestion.pipeline import IngestionPipeline
from ingestion.video_reader import VideoReader


def create_test_video(path: Path, fps: int = 4) -> Path:
    writer = cv2.VideoWriter(
        str(path),
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (64, 64),
    )

    for index in range(12):
        if index < 8:
            frame = np.full((64, 64, 3), 40, dtype=np.uint8)
        else:
            frame = np.full((64, 64, 3), 220, dtype=np.uint8)
            cv2.rectangle(frame, (8, 8), (56, 56), (20, 20, 20), -1)
        writer.write(frame)

    writer.release()
    return path


def test_video_reader_extracts_metadata(tmp_path: Path) -> None:
    video_path = create_test_video(tmp_path / "sample.mp4")

    metadata = VideoReader().read_metadata(video_path)

    assert metadata.filename == "sample.mp4"
    assert metadata.fps == 4
    assert metadata.frame_count == 12
    assert metadata.width == 64
    assert metadata.height == 64
    assert metadata.duration_sec == 3


def test_pipeline_extracts_and_deduplicates_frames(tmp_path: Path) -> None:
    video_path = create_test_video(tmp_path / "sample.mp4")
    frame_dir = tmp_path / "frames"

    result = IngestionPipeline(
        frame_dir=frame_dir,
        sample_rate=1,
        dedup_threshold=5,
    ).process(video_path)

    assert result.extracted_count == 3
    assert result.kept_count == 2
    assert result.skipped_duplicates == 1
    assert result.manifest_path is not None
    assert result.manifest_path.exists()
    assert [frame.timestamp_sec for frame in result.frames] == [0.0, 2.0]
    assert all(frame.path.exists() for frame in result.frames)
