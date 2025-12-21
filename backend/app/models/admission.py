from sqlalchemy import Column, Integer, String, ForeignKey, Date, Enum
from app.database.base import Base
import enum

class AdmissionStatus(enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

class Admission(Base):
    __tablename__ = "admissions"
    id = Column(
        Integer,
        primary_key=True,
        index=True,
        doc="Unique admission ID (Primary Key, required)"
    )
    student_id = Column(
        Integer,
        ForeignKey("students.id"),
        nullable=False,
        doc="Reference to students.id (required)"
    )
    application_date = Column(
        Date,
        nullable=False,
        doc="Date of application (required)"
    )
    status = Column(
        Enum(AdmissionStatus),
        default=AdmissionStatus.PENDING,
        nullable=False,
        doc="Admission status (required, default 'PENDING')"
    )