
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy import select
from app.models.teacher import Teacher
from app.schemas.teacher import TeacherCreate
from typing import List, Dict, Any

async def create_teacher(db: AsyncSession, teacher_data: TeacherCreate) -> Teacher:
    """
    Create a new teacher with validation and robust error handling.
    Raises ValueError for validation or DB errors.
    """
    try:
        data = teacher_data.dict()
        required_fields = ["user_id", "subject_id", "name"]
        for field in required_fields:
            if not data.get(field):
                raise ValueError(f"{field} is required.")
        # Validate ID types
        if not isinstance(data["user_id"], str):
            raise ValueError("user_id must be a string.")
        if not isinstance(data["subject_id"], str):
            raise ValueError("subject_id must be a string.")
        teacher = Teacher(**data)
        db.add(teacher)
        await db.commit()
        await db.refresh(teacher)
        return teacher
    except IntegrityError as e:
        await db.rollback()
        msg = str(e).lower()
        if "user_id" in msg:
            raise ValueError("Teacher with this user_id already exists.")
        raise ValueError("Teacher creation failed due to duplicate data")
    except SQLAlchemyError as e:
        await db.rollback()
        raise ValueError(f"Database error: {str(e)}")
    except Exception as e:
        await db.rollback()
        raise ValueError(f"Unexpected error creating teacher: {str(e)}")

async def get_teachers(db: AsyncSession) -> List[Teacher]:
    """
    Fetch all teachers from the database.
    Returns a list of Teacher objects.
    Raises ValueError on database errors.
    """
    try:
        result = await db.execute(select(Teacher))
        teachers = result.scalars().all()
        return teachers
    except SQLAlchemyError as e:
        raise ValueError(f"Error fetching teachers: {str(e)}")
    except Exception as e:
        raise ValueError(f"Unexpected error fetching teachers: {str(e)}")

async def get_teacher_by_id(db: AsyncSession, teacher_id: str) -> Teacher:
    """
    Fetch a teacher by ID. Raises ValueError if not found or on DB error.
    """
    try:
        teacher = await db.get(Teacher, teacher_id)
        if not teacher:
            raise ValueError("Teacher not found")
        return teacher
    except SQLAlchemyError as e:
        raise ValueError(f"Database error: {str(e)}")
    except Exception as e:
        raise ValueError(f"Unexpected error fetching teacher: {str(e)}")