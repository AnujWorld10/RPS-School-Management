from pydantic import BaseModel, Field
from datetime import date

class AttendanceBase(BaseModel):
    student_id: str
    date: date
    present: bool = True

class AttendanceCreate(AttendanceBase):
    pass

class AttendanceResponse(AttendanceBase):
    id: str
    class Config:
        from_attributes = True
