from sqlalchemy import Column, Integer, String, Date
from app.database.base import Base

class RemovedStudent(Base):
    __tablename__ = "removed_students"
    id = Column(
        Integer,
        primary_key=True,
        index=True,
        doc="Unique removed student ID (Primary Key, required)"
    )
    name = Column(
        String(255),
        nullable=False,
        doc="Removed student's full name (required, max 255 chars)"
    )
    reason = Column(
        String(255),
        nullable=True,
        doc="Reason for removal (optional, max 255 chars)"
    )
    removal_date = Column(
        Date,
        nullable=False,
        doc="Date of removal (required)"
    )
    # Copy key fields from students for archiving