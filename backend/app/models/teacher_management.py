"""
TeacherManagement model for assigning teachers to classes and subjects.
"""
from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database.base import Base
from datetime import datetime

class TeacherManagement(Base):
    __tablename__ = "teacher_management"
    id = Column(
        String(10),
        primary_key=True,
        index=True,
        unique=True,
        doc="Unique teacher management ID (Primary Key, required, format: Rps_XXXXX)"
    )
    teacher_id = Column(
        String(10),
        ForeignKey("teachers.id"),
        nullable=False,
        doc="Reference to teachers.id (required, format: Rps_XXXXX)"
    )
    class_id = Column(
        String(10),
        ForeignKey("classes.id"),
        nullable=False,
        doc="Reference to classes.id (required, format: Rps_XXXXX)"
    )
    subject_id = Column(
        String(3),
        ForeignKey("subjects.id"),
        nullable=False,
        doc="Reference to subjects.id (required, 3-digit string)"
    )
    assigned_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        doc="Timestamp when assignment was made (required)"
    )
    teacher = relationship("Teacher")
    class_rel = relationship("Class")
    subject = relationship("Subject")
