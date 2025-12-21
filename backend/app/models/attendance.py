from sqlalchemy import Column, Integer, ForeignKey, Date, Boolean
from app.database.base import Base

class Attendance(Base):
    __tablename__ = "attendance"
    id = Column(
        Integer,
        primary_key=True,
        index=True,
        doc="Unique attendance ID (Primary Key, required)"
    )
    student_id = Column(
        Integer,
        ForeignKey("students.id"),
        nullable=False,
        doc="Reference to students.id (required)"
    )
    date = Column(
        Date,
        nullable=False,
        doc="Attendance date (required)"
    )
    present = Column(
        Boolean,
        default=True,
        nullable=False,
        doc="Is the student present? (required, default True)"
    )