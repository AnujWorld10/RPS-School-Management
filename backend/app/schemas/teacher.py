from pydantic import BaseModel
from datetime import date

class TeacherCreate(BaseModel):
    user_id: str
    subject_id: str
    name: str
    joining_date: date
    salary: int
    qualifications: str

class TeacherResponse(BaseModel):
    id: str
    name: str
    subject: str