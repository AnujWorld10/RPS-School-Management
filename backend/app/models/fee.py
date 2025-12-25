from sqlalchemy import Column, Integer, String, ForeignKey, Float, Enum
from app.database.base import Base
import enum

class FeeStatus(enum.Enum):
    PAID = "PAID"
    PENDING = "PENDING"
    DUE = "DUE"

class Fee(Base):
    __tablename__ = "fees"
    id = Column(
        String(10),
        primary_key=True,
        index=True,
        unique=True,
        doc="Unique fee ID (Primary Key, required, format: Rps_XXXXX)"
    )
    student_id = Column(
        String(10),
        ForeignKey("students.id"),
        nullable=False,
        doc="Reference to students.id (required, format: Rps_XXXXX)"
    )
    amount = Column(
        Float,
        nullable=False,
        doc="Fee amount (required)"
    )
    month = Column(
        String(20),
        nullable=False,
        doc="Fee month (required, e.g., '2023-10', max 20 chars)"
    )
    status = Column(
        Enum(FeeStatus),
        default=FeeStatus.PENDING,
        nullable=False,
        doc="Fee status (required, default 'PENDING')"
    )