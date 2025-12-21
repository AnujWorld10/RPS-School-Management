from pydantic import BaseModel
from datetime import date

class TeacherCreate(BaseModel):
    user_id: int
    subject_id: int
    name: str
    joining_date: date
    salary: int
    qualifications: str

class TeacherResponse(BaseModel):
    id: int
    name: str
    subject: str