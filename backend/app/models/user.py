from sqlalchemy import Column, Integer, String, Boolean, Enum, DateTime
from sqlalchemy.sql import func
from app.database.base import Base
import enum

class Role(enum.Enum):
    ADMIN = "ADMIN"
    TEACHER = "TEACHER"
    STUDENT = "STUDENT"

class User(Base):
    __tablename__ = "users"
    id = Column(
        Integer,
        primary_key=True,
        index=True,
        doc="Unique user ID (Primary Key, required)"
    )
    username = Column(
        String(50),
        unique=True,
        index=True,
        nullable=False,
        doc="Unique username used for login (required, max 50 chars)"
    )
    password_hash = Column(
        String(255),
        nullable=False,
        doc="Hashed password (required, max 255 chars)"
    )
    role = Column(
        Enum(Role),
        nullable=False,
        doc="Role of the user (admin, teacher, student) (required)"
    )
    is_active = Column(
        Boolean,
        default=True,
        nullable=False,
        doc="Is the user active? (required, default True)"
    )
    created_at = Column(
        DateTime,
        default=func.now(),
        nullable=False,
        doc="Timestamp when user was created (required)"
    )
    updated_at = Column(
        DateTime,
        default=func.now(),
        onupdate=func.now(),
        nullable=False,
        doc="Timestamp when user was last updated (required)"
    )