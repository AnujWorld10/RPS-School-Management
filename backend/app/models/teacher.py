from sqlalchemy import Column, Date, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.database.base import Base

class Teacher(Base):
    __tablename__ = "teachers"
    id = Column(
        Integer,
        primary_key=True,
        index=True,
        doc="Unique teacher ID (Primary Key, required)"
    )
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        unique=True,
        nullable=False,
        doc="Reference to users.id (required, unique)"
    )
    name = Column(
        String(255),
        nullable=False,
        doc="Teacher's full name (required, max 255 chars)"
    )
    subject_id = Column(
        Integer,
        ForeignKey("subjects.id"),
        nullable=False,
        doc="Reference to subjects.id (required)"
    )
    salary = Column(
        Float,
        nullable=True,
        doc="Salary of the teacher (optional)"
    )
    joining_date = Column(
        Date,
        nullable=True,
        doc="Date of joining (optional)"
    )
    user = relationship("User")
    subject = relationship("Subject")