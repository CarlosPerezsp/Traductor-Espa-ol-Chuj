from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from pydantic import BaseModel
import os

from app.database import get_db
from app.models import Translation, Language

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


@app.get("/api/health")
def health():
    return {"status": "ok", "message": "Hello from backend"}


class TranslateRequest(BaseModel):
    text: str
    source_lang: str = "es"
    target_lang: str = "chuj"


@app.post("/api/translate")
def translate(req: TranslateRequest, db: Session = Depends(get_db)):
    src = db.query(Language).filter(Language.code == req.source_lang).first()
    tgt = db.query(Language).filter(Language.code == req.target_lang).first()
    if not src or not tgt:
        raise HTTPException(status_code=404, detail="Language not found")

    result = (
        db.query(Translation)
        .filter(
            Translation.source_lang == src.id,
            Translation.target_lang == tgt.id,
            Translation.source_text.ilike(req.text.strip()),
        )
        .first()
    )

    if not result:
        raise HTTPException(status_code=404, detail="Translation not found")

    return {
        "source_text": result.source_text,
        "target_text": result.target_text,
        "source_lang": req.source_lang,
        "target_lang": req.target_lang,
    }


@app.get("/api/translations")
def list_translations(
    source_lang: str = "es",
    target_lang: str = "chuj",
    db: Session = Depends(get_db),
):
    src = db.query(Language).filter(Language.code == source_lang).first()
    tgt = db.query(Language).filter(Language.code == target_lang).first()
    if not src or not tgt:
        raise HTTPException(status_code=404, detail="Language not found")

    rows = (
        db.query(Translation)
        .filter(
            Translation.source_lang == src.id,
            Translation.target_lang == tgt.id,
        )
        .all()
    )
    return [
        {"id": r.id, "source_text": r.source_text, "target_text": r.target_text}
        for r in rows
    ]
