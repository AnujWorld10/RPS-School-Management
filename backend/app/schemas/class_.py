from pydantic import BaseModel, Field

class ClassBase(BaseModel):
    name: str = Field(..., max_length=100, description="Class name (e.g., 1st Grade)")
    section: str | None = Field(None, max_length=50, description="Section (e.g., A, B)")
    description: str | None = Field(None, max_length=255, description="Optional class description")
    class_teacher_id: str = Field(..., max_length=10, description="ID of the class teacher (Rps_XXXXX)")

class ClassCreate(ClassBase):
    pass

class ClassResponse(ClassBase):
    id: str
    class Config:
        from_attributes = True
