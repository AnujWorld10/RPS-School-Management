from pydantic import BaseModel, Field

class ResultBase(BaseModel):
    student_id: str
    subject_id: int
    exam_name: str
    marks: float
    grade: str | None = None

class ResultCreate(ResultBase):
    pass

class ResultResponse(ResultBase):
    id: str
    class Config:
        from_attributes = True
