from sqlalchemy import Column, Integer, String
from app.database.base import Base

class Class(Base):
    __tablename__ = "classes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)  # e.g., "Class 10A"
    section = Column(String)  # e.g., "A"