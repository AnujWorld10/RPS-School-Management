from sqlalchemy import Column, Integer, String, Float, Date
from app.database.base import Base

class Employee(Base):
    __tablename__ = "employees"
    id = Column(
        Integer,
        primary_key=True,
        index=True,
        doc="Unique employee ID (Primary Key, required)"
    )
    name = Column(
        String(255),
        nullable=False,
        doc="Employee's full name (required, max 255 chars)"
    )
    role = Column(
        String(50),
        nullable=False,
        doc="Role of the employee (required, e.g., 'Librarian', max 50 chars)"
    )
    salary = Column(
        Float,
        nullable=True,
        doc="Salary of the employee (optional)"
    )
    joining_date = Column(
        Date,
        nullable=True,
        doc="Date of joining (optional)"
    )