from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Language, Translation


router = APIRouter(prefix="/api", tags=["translations"])


class TranslateRequest(BaseModel):
    text: str
    source_lang: str = "es"
    target_lang: str = "chuj"


@router.post("/translate")
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


@router.get("/translations")
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
