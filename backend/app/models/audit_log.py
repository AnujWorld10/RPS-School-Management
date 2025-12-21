from sqlalchemy import Column, Integer, String, DateTime
from app.database.base import Base
from datetime import datetime

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(
        Integer,
        primary_key=True,
        index=True,
        doc="Unique audit log ID (Primary Key, required)"
    )
    action = Column(
        String(100),
        nullable=False,
        doc="Action performed (required, max 100 chars)"
    )
    user_id = Column(
        Integer,
        nullable=False,
        doc="User ID who performed the action (required)"
    )
    timestamp = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        doc="Timestamp of the action (required)"
    )
    details = Column(
        String(255),
        nullable=True,
        doc="Additional details (optional, max 255 chars)"
    )
