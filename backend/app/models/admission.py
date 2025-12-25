from sqlalchemy import Column, Integer, String, ForeignKey, Date, Enum
from app.database.base import Base
import enum

class AdmissionStatus(enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

class Admission(Base):
    __tablename__ = "admissions"
    admission_id = Column(
        String(10),
        primary_key=True,
        index=True,
        unique=True,
        doc="Unique admission ID (Primary Key, required, format: Rps_XXXXXX)"
    )
    student_id = Column(
        String(10),
        ForeignKey("students.id"),
        nullable=False,
        doc="Reference to students.id (required, format: Rps_XXXXX)"
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