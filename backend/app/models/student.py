from app.models.class_ import Class  # noqa: F401
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.database.base import Base

class Student(Base):
    __tablename__ = "students"
    id = Column(
        Integer,
        primary_key=True,
        index=True,
        doc="Unique student ID (Primary Key, required)"
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
        doc="Student's full name (required, max 255 chars)"
    )
    dob = Column(
        Date,
        nullable=True,
        doc="Date of birth (optional)"
    )
    address = Column(
        String(255),
        nullable=True,
        doc="Home address (optional, max 255 chars)"
    )
    phone = Column(
        String(20),
        nullable=True,
        doc="Contact phone number (optional, max 20 chars)"
    )
    class_id = Column(
        Integer,
        ForeignKey("classes.id"),
        nullable=False,
        doc="Reference to classes.id (required)"
    )
    admission_date = Column(
        Date,
        nullable=True,
        doc="Date of admission (optional)"
    )
    user = relationship("User")
    class_rel = relationship("Class"
                             )
    roll_number = Column(String(50), 
        nullable=False, 
        unique=True, 
        doc="Unique roll number for the student (required, max 50 chars)"
        )
    email = Column(
    String(255),
    unique=True,
    nullable=False,
    doc="Student email address"
    )