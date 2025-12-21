from sqlalchemy import Column, Integer, String
from app.database.base import Base

class Subject(Base):
    __tablename__ = "subjects"
    id = Column(
        Integer,
        primary_key=True,
        index=True,
        doc="Unique subject ID (Primary Key, required)"
    )
    name = Column(
        String(100),
        unique=True,
        nullable=False,
        doc="Subject name (required, unique, max 100 chars)"
    )  # e.g., "Mathematics"