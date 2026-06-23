from pathlib import Path

from fastapi.testclient import TestClient

from api.config import Settings, get_settings
from api.main import app
from tests.test_ingestion import create_test_video


def test_upload_rejects_unsupported_file(tmp_path: Path) -> None:
    settings = Settings(upload_dir=tmp_path / "uploads", frame_dir=tmp_path / "frames")
    app.dependency_overrides[get_settings] = lambda: settings

    client = TestClient(app)
    response = client.post(
        "/videos/upload",
        files={"video": ("notes.txt", b"not a video", "text/plain")},
    )

    app.dependency_overrides.clear()

    assert response.status_code == 400
    assert response.json()["detail"] == "Unsupported video format"


def test_upload_processes_video(tmp_path: Path) -> None:
    video_path = create_test_video(tmp_path / "sample.mp4")
    settings = Settings(upload_dir=tmp_path / "uploads", frame_dir=tmp_path / "frames")
    app.dependency_overrides[get_settings] = lambda: settings

    client = TestClient(app)
    with video_path.open("rb") as handle:
        response = client.post(
            "/videos/upload",
            files={"video": ("sample.mp4", handle, "video/mp4")},
        )

    app.dependency_overrides.clear()

    body = response.json()
    assert response.status_code == 201
    assert body["video"]["filename"].endswith(".mp4")
    assert body["summary"]["extracted_count"] == 3
    assert body["summary"]["kept_count"] == 2
    assert body["summary"]["skipped_duplicates"] == 1
    assert body["manifest_path"].endswith("metadata.json")
