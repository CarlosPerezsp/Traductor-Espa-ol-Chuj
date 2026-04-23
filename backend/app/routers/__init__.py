from app.routers.translations import router as translations_router
from app.routers.languages import router as languages_router
from app.routers.upload import router as upload_router

__all__ = ["translations_router", "languages_router", "upload_router"]
