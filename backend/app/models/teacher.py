from sqlalchemy import Column, Date, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.database.base import Base

class Teacher(Base):   
    __tablename__ = "teachers"
    id = Column(
        String(10),
        primary_key=True,
        index=True,
        unique=True,
        doc="Unique teacher ID (Primary Key, required, format: Rps_XXXXX)"
    )
    class_id = Column(
            String(10),
            unique=True,
            nullable=True,
            doc="ID of the class this teacher is assigned to as class teacher (Rps_XXXXX)"
        )
    user_id = Column(
        String(10),
        ForeignKey("users.id"),
        unique=True,
        nullable=False,
        doc="Reference to users.id (required, unique, format: Rps_XXXXX)"
    )
    name = Column(
        String(255),
        nullable=False,
        doc="Teacher's full name (required, max 255 chars)"
    )
    subject_id = Column(
        String(3),
        ForeignKey("subjects.id"),
        nullable=False,
        doc="Reference to subjects.id (required, 3-digit string)"
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