from enum import Enum

class RoleEnum(str, Enum):
    ADMIN = "ADMIN"
    OFFICE_STAFF = "OFFICE_STAFF"
    TEACHER = "TEACHER"
    STUDENT = "STUDENT"
