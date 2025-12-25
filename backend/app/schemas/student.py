from pydantic import BaseModel
from datetime import date

class StudentCreate(BaseModel):
    user_id: int
    class_id: int
    name: str
    roll_number: str
    admission_date: date
    address: str
    phone: str
    email: str

class StudentResponse(BaseModel):
    id: str
    user_id: str
    class_id: str
    name: str
    roll_number: str
    class_name: str