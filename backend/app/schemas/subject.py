"""
Subject schema for validation and serialization.
"""
from pydantic import BaseModel, Field, validator

class SubjectBase(BaseModel):
    name: str = Field(..., max_length=100, description="Subject name (required, unique, max 100 chars)")

class SubjectCreate(SubjectBase):
    pass

class SubjectResponse(SubjectBase):
    id: str = Field(..., regex=r"^\d{3}$", description="Unique 3-digit subject ID (required)")
    class Config:
        from_attributes = True

    @validator('id')
    def id_must_be_3_digits(cls, v):
        if not (isinstance(v, str) and len(v) == 3 and v.isdigit()):
            raise ValueError('Subject ID must be a 3-digit string')
        return v
