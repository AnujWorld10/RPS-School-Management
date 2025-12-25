from pydantic import BaseModel, Field
from datetime import date

class EmployeeBase(BaseModel):
    name: str
    role: str
    salary: float | None = None
    joining_date: date | None = None

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeResponse(EmployeeBase):
    id: str
    class Config:
        from_attributes = True
