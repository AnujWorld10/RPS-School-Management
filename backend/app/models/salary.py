from sqlalchemy import Column, Integer, Float, ForeignKey
from app.database.base import Base

class Salary(Base):
    __tablename__ = "salaries"
    id = Column(
        Integer,
        primary_key=True,
        index=True,
        doc="Unique salary ID (Primary Key, required)"
    )
    employee_id = Column(
        Integer,
        ForeignKey("employees.id"),
        nullable=False,
        doc="Reference to employees.id (required)"
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
