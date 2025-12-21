from pydantic import BaseModel
from datetime import date

class FeeCreate(BaseModel):
    student_id: int
    amount: float
    month: str
    status: str
    due_date: date