from sqlalchemy import Column, Integer, ForeignKey, Date, Boolean, String
from app.database.base import Base

class Attendance(Base):
    __tablename__ = "attendance"
    id = Column(
        String(10),
        primary_key=True,
        index=True,
        unique=True,
        doc="Unique attendance ID (Primary Key, required, format: Rps_XXXXX)"
    )
    student_id = Column(
        String(10),
        ForeignKey("students.id"),
        nullable=False,
        doc="Reference to students.id (required, format: Rps_XXXXX)"
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