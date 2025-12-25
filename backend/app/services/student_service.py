
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy import select
from app.models.student import Student
from app.schemas.student import StudentCreate
from typing import List, Dict, Any

async def create_student(db: AsyncSession, student_data: StudentCreate) -> Student:
    """
    Create a new student with validation and robust error handling.
    Raises ValueError for validation or DB errors.
    """
    try:
        # Validate required fields
        data = student_data.dict()
        required_fields = ["user_id", "class_id", "name", "roll_number"]
        for field in required_fields:
            if not data.get(field):
                raise ValueError(f"{field} is required.")
        # Validate ID types
        if not isinstance(data["user_id"], str):
            raise ValueError("user_id must be a string.")
        if not isinstance(data["class_id"], str):
            raise ValueError("class_id must be a string.")
        # Validate roll_number uniqueness (optional, for early feedback)
        stmt = select(Student).where(Student.roll_number == data["roll_number"])
        result = await db.execute(stmt)
        if result.scalars().first():
            raise ValueError("Student with this roll number already exists.")
        student = Student(**data)
        db.add(student)
        await db.commit()
        await db.refresh(student)
        return student
    except IntegrityError as e:
        await db.rollback()
        msg = str(e).lower()
        if "roll_number" in msg:
            raise ValueError("Student with this roll number already exists.")
        elif "user_id" in msg:
            raise ValueError("Student with this user_id already exists.")
        raise ValueError(f"Database integrity error: {str(e)}")
    except SQLAlchemyError as e:
        await db.rollback()
        raise ValueError(f"Database error: {str(e)}")
    except Exception as e:
        await db.rollback()
        raise ValueError(f"Unexpected error creating student: {str(e)}")

async def get_students(db: AsyncSession) -> List[Student]:
    """
    Fetch all students from the database.
    Returns a list of Student objects.
    Raises ValueError on database errors.
    """
    try:
        result = await db.execute(select(Student))
        students = result.scalars().all()
        return students
    except SQLAlchemyError as e:
        raise ValueError(f"Error fetching students: {str(e)}")
    except Exception as e:
        raise ValueError(f"Unexpected error fetching students: {str(e)}")

async def get_student_by_id(db: AsyncSession, student_id: str) -> Student:
    """
    Fetch a student by ID. Raises ValueError if not found or on DB error.
    """
    try:
        student = await db.get(Student, student_id)
        if not student:
            raise ValueError("Student not found")
        return student
    except SQLAlchemyError as e:
        raise ValueError(f"Database error: {str(e)}")
    except Exception as e:
        raise ValueError(f"Unexpected error fetching student: {str(e)}")

async def update_student(db: AsyncSession, student_id: str, update_data: Dict[str, Any]) -> Student:
    """
    Update a student's information. Raises ValueError on errors.
    """
    try:
        student = await db.get(Student, student_id)
        if not student:
            raise ValueError("Student not found")
        for key, value in update_data.items():
            if hasattr(student, key):
                setattr(student, key, value)
        await db.commit()
        await db.refresh(student)
        return student
    except SQLAlchemyError as e:
        await db.rollback()
        raise ValueError(f"Update error: {str(e)}")
    except Exception as e:
        await db.rollback()
        raise ValueError(f"Unexpected error updating student: {str(e)}")

async def delete_student(db: AsyncSession, student_id: str) -> Dict[str, str]:
    """
    Delete a student by ID. Raises ValueError on errors.
    """
    try:
        student = await db.get(Student, student_id)
        if not student:
            raise ValueError("Student not found")
        await db.delete(student)
        await db.commit()
        return {"message": "Student deleted"}
    except SQLAlchemyError as e:
        await db.rollback()
        raise ValueError(f"Delete error: {str(e)}")
    except Exception as e:
        await db.rollback()
        raise ValueError(f"Unexpected error deleting student: {str(e)}")