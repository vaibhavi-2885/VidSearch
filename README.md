# VidSearch

Self-hosted multimodal video search engine.

## Current Setup

- Python virtual environment: `venv`
- FastAPI backend: `api/main.py`
- Streamlit frontend: `frontend/app.py`
- Qdrant vector database: `localhost:6333`
- Redis queue/cache: `localhost:6379`
- Local storage folders: `data/uploads`, `data/frames`, `data/temp`

## VS Code Terminal Commands

Activate the environment:

```powershell
.\venv\Scripts\Activate.ps1
```

Run setup tests:

```powershell
python -m pytest tests\test_setup.py -q
python tests\check_services.py
```

Run the backend:

```powershell
python -m uvicorn api.main:app --reload --host 127.0.0.1 --port 8000
```

Open:

```text
http://127.0.0.1:8000/health
http://127.0.0.1:8000/docs
```

Run the frontend in another terminal:

```powershell
streamlit run frontend/app.py
```

Open:

```text
http://localhost:8501
```

## Docker Services

Qdrant and Redis are required for the full project.

If they are not already running, use:

```powershell
docker compose up -d
```

Check running containers:

```powershell
docker ps
```

Qdrant dashboard:

```text
http://localhost:6333/dashboard
```

## Next Build Step

The first real implementation step is the ingestion pipeline:

1. Accept video uploads.
2. Extract metadata.
3. Extract frames at 1 FPS.
4. Deduplicate similar frames with ImageHash.
5. Save frame paths and timestamps.
