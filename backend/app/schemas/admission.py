from pydantic import BaseModel, Field
from datetime import date
from enum import Enum

class AdmissionStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

class AdmissionBase(BaseModel):
    student_id: str = Field(..., max_length=10, description="Student ID (Rps_XXXXX)")
    application_date: date
    status: AdmissionStatus = AdmissionStatus.PENDING

class AdmissionCreate(AdmissionBase):
    pass

class AdmissionResponse(AdmissionBase):
    admission_id: str
    class Config:
        from_attributes = True
