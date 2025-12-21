from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.models.student import Student
from app.models.admission import Admission
from app.schemas.student import StudentCreate, StudentResponse

async def create_student(db: AsyncSession, student_data: StudentCreate):
    try:
        student = Student(**student_data.dict())
        db.add(student)
        await db.commit()
        await db.refresh(student)
        return student
    except IntegrityError as e:
        await db.rollback()
        msg = str(e).lower()
        if "roll_number" in msg:
            raise ValueError("Student with this roll number already exists")
        elif "user_id" in msg:
            raise ValueError("Student with this user_id already exists")
        elif "email" in msg:
            raise ValueError("Student with this email already exists")
        raise ValueError(f"Database integrity error: {str(e)}")
    except SQLAlchemyError as e:
        await db.rollback()
        raise ValueError(f"Database error: {str(e)}")

async def get_students(db: AsyncSession):
    """
    Fetch all students from the database using async SQLAlchemy.
    Returns a list of Student objects.
    Raises ValueError on database errors.
    """
    from sqlalchemy import select
    try:
        # Use async select for SQLAlchemy 1.4+ async support
        result = await db.execute(select(Student))
        students = result.scalars().all()
        return students
    except SQLAlchemyError as e:
        # Handle SQLAlchemy-specific errors
        raise ValueError(f"Error fetching students: {str(e)}")
    except Exception as e:
        # Handle any other unexpected errors
        raise ValueError(f"Unexpected error fetching students: {str(e)}")

async def get_student_by_id(db: AsyncSession, student_id: int):
    try:
        student = await db.get(Student, student_id)
        if not student:
            raise ValueError("Student not found")
        return student
    except SQLAlchemyError as e:
        raise ValueError(f"Database error: {str(e)}")

async def update_student(db: AsyncSession, student_id: int, update_data: dict):
    try:
        student = await db.get(Student, student_id)
        if not student:
            raise ValueError("Student not found")
        for key, value in update_data.items():
            setattr(student, key, value)
        await db.commit()
        await db.refresh(student)
        return student
    except SQLAlchemyError as e:
        await db.rollback()
        raise ValueError(f"Update error: {str(e)}")

async def delete_student(db: AsyncSession, student_id: int):
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