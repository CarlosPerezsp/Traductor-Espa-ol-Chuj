from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Language


router = APIRouter(prefix="/api/languages", tags=["languages"])


@router.get("/")
def list_languages(db: Session = Depends(get_db)):
    rows = db.query(Language).all()
    return [{"id": r.id, "code": r.code, "name": r.name} for r in rows]
