from sqlalchemy import Column, Integer, String, ForeignKey, Float
from app.database.base import Base

class Result(Base):
    __tablename__ = "results"
    id = Column(
        String(10),
        primary_key=True,
        index=True,
        unique=True,
        doc="Unique result ID (Primary Key, required, format: Rps_XXXXX)"
    )
    student_id = Column(
        String(10),
        ForeignKey("students.id"),
        nullable=False,
        doc="Reference to students.id (required, format: Rps_XXXXX)"
    )
    subject_id = Column(
        String(3),
        ForeignKey("subjects.id"),
        nullable=False,
        doc="Reference to subjects.id (required, 3-digit string)"
    )
    exam_name = Column(
        String(100),
        nullable=False,
        doc="Exam name (required, max 100 chars)"
    )
    marks = Column(
        Float,
        nullable=False,
        doc="Marks obtained (required)"
    )
    grade = Column(
        String(10),
        nullable=True,
        doc="Grade (optional, max 10 chars)"
    )