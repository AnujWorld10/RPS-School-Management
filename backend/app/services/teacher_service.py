from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.models.teacher import Teacher
from app.schemas.teacher import TeacherCreate

async def create_teacher(db: AsyncSession, teacher_data: TeacherCreate):
    try:
        teacher = Teacher(**teacher_data.dict())
        db.add(teacher)
        await db.commit()
        await db.refresh(teacher)
        return teacher
    except IntegrityError as e:
        await db.rollback()
        raise ValueError("Teacher creation failed due to duplicate data")
    except SQLAlchemyError as e:
        await db.rollback()
        raise ValueError(f"Database error: {str(e)}")

async def get_teachers(db: AsyncSession):
    try:
        teachers = await db.query(Teacher).all()
        return teachers
    except SQLAlchemyError as e:
        raise ValueError(f"Error fetching teachers: {str(e)}")

async def get_teacher_by_id(db: AsyncSession, teacher_id: int):
    try:
        teacher = await db.get(Teacher, teacher_id)
        if not teacher:
            raise ValueError("Teacher not found")
        return teacher
    except SQLAlchemyError as e:
        raise ValueError(f"Database error: {str(e)}")