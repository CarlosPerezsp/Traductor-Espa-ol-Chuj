from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Language(Base):
    __tablename__ = "languages"

    id   = Column(Integer, primary_key=True, index=True)
    code = Column(String(10), unique=True, nullable=False)
    name = Column(String(100), nullable=False)


class Category(Base):
    __tablename__ = "categories"

    id   = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)


class Translation(Base):
    __tablename__ = "translations"

    id          = Column(Integer, primary_key=True, index=True)
    source_text = Column(String(500), nullable=False)
    target_text = Column(String(500), nullable=False)
    source_lang = Column(Integer, ForeignKey("languages.id"), nullable=False)
    target_lang = Column(Integer, ForeignKey("languages.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    notes       = Column(Text, nullable=True)
    created_at  = Column(TIMESTAMP, server_default=func.now())

    source_language = relationship("Language", foreign_keys=[source_lang])
    target_language = relationship("Language", foreign_keys=[target_lang])
    category        = relationship("Category")
