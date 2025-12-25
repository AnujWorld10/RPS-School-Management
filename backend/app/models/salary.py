from sqlalchemy import Column, Integer, Float, ForeignKey, String
from app.database.base import Base

class Salary(Base):
    __tablename__ = "salaries"
    id = Column(
        String(10),
        primary_key=True,
        index=True,
        unique=True,
        doc="Unique salary ID (Primary Key, required, format: Rps_XXXXX)"
    )
    employee_id = Column(
        String(10),
        ForeignKey("employees.id"),
        nullable=False,
        doc="Reference to employees.id (required, format: Rps_XXXXX)"
    )
    amount = Column(
        Float,
        nullable=False,
        doc="Salary amount (required)"
    )
    month = Column(
        Integer,
        nullable=False,
        doc="Salary month (required, e.g., 202312 for December 2023)"
    )
