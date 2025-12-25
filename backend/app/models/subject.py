from sqlalchemy import Column, Integer, String
from app.database.base import Base

import random
from sqlalchemy import event

class Subject(Base):
    __tablename__ = "subjects"
    id = Column(
        String(3),
        primary_key=True,
        index=True,
        unique=True,
        doc="Unique subject ID (Primary Key, required, 3-digit string)"
    )
    name = Column(
        String(100),
        unique=True,
        nullable=False,
        doc="Subject name (required, unique, max 100 chars)"
    )  # e.g., "Mathematics"

# Auto-generate unique 3-digit string ID for Subject
@event.listens_for(Subject, "before_insert")
def generate_subject_id(mapper, connection, target):
    if not target.id:
        # Try up to 10 times to avoid collision
        for _ in range(10):
            new_id = f"{random.randint(0, 999):03}"
            existing = connection.execute(
                Subject.__table__.select().where(Subject.id == new_id)
            ).fetchone()
            if not existing:
                target.id = new_id
                break
        else:
            raise Exception("Failed to generate unique 3-digit subject ID after 10 attempts.")