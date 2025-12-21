# Renamed from class.py to class_.py to avoid Python keyword conflict
from sqlalchemy import Column, Integer, String
from app.database.base import Base

class Class(Base):
    __tablename__ = "classes"
    id = Column(
        Integer,
        primary_key=True,
        index=True,
        doc="Unique class ID (Primary Key, required)"
    )
    name = Column(
        String(100),
        unique=True,
        index=True,
        nullable=False,
        doc="Class name (required, unique, max 100 chars)"
    )
    description = Column(
        String(255),
        nullable=True,
        doc="Class description (optional, max 255 chars)"
    )
