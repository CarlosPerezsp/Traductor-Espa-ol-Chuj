from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.routers import translations_router, languages_router

app = FastAPI(title="ALMG API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve uploaded/static media files
os.makedirs("/app/media", exist_ok=True)
app.mount("/media", StaticFiles(directory="/app/media"), name="media")

app.include_router(translations_router)
app.include_router(languages_router)


@app.get("/api/health")
def health():
    return {"status": "ok", "message": "Hello from backend"}
