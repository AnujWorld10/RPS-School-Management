from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

class Role(str, Enum):
    ADMIN = "ADMIN"
    TEACHER = "TEACHER"
    STUDENT = "STUDENT"


from pydantic import EmailStr, validator

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    role: Role

    @validator('role')
    def validate_role(cls, v):
        allowed = {Role.ADMIN, Role.TEACHER, Role.STUDENT}
        if v not in allowed:
            raise ValueError('Role must be ADMIN, TEACHER, or STUDENT')
        return v


class UserResponse(BaseModel):
    id: str
    username: str
    email: EmailStr
    role: Role
    is_active: bool = True
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True
