from fastapi import FastAPI

from api.routes_upload import router as upload_router

app = FastAPI(title="VidSearch API", version="0.1.0")
app.include_router(upload_router)


@app.get("/")
async def root() -> dict:
    return {
        "app": "VidSearch API",
        "status": "running",
        "docs": "/docs",
        "health": "/health",
        "upload": "/videos/upload",
    }


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
