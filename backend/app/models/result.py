from sqlalchemy import Column, Integer, String, ForeignKey, Float
from app.database.base import Base

class Result(Base):
    __tablename__ = "results"
    id = Column(
        Integer,
        primary_key=True,
        index=True,
        doc="Unique result ID (Primary Key, required)"
    )
    student_id = Column(
        Integer,
        ForeignKey("students.id"),
        nullable=False,
        doc="Reference to students.id (required)"
    )
    subject_id = Column(
        Integer,
        ForeignKey("subjects.id"),
        nullable=False,
        doc="Reference to subjects.id (required)"
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