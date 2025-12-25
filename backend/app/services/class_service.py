
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy import select
from app.models.class_ import Class
from app.schemas.class_ import ClassCreate
from typing import List

async def create_class(db: AsyncSession, class_data: ClassCreate) -> Class:
    """
    Create a new class with validation and robust error handling.
    Raises ValueError for validation or DB errors.
    """
    try:
        data = class_data.dict()
        required_fields = ["name", "class_teacher_id"]
        for field in required_fields:
            if not data.get(field):
                raise ValueError(f"{field} is required.")
        # Validate name uniqueness (optional, for early feedback)
        stmt = select(Class).where(Class.name == data["name"])
        result = await db.execute(stmt)
        if result.scalars().first():
            raise ValueError("Class with this name already exists.")
        new_class = Class(**data)
        db.add(new_class)
        await db.commit()
        await db.refresh(new_class)
        return new_class
    except IntegrityError as e:
        await db.rollback()
        msg = str(e).lower()
        if "unique" in msg and "name" in msg:
            raise ValueError("Class with this name already exists.")
        raise ValueError(f"Database integrity error: {str(e)}")
    except SQLAlchemyError as e:
        await db.rollback()
        raise ValueError(f"Database error: {str(e)}")
    except Exception as e:
        await db.rollback()
        raise ValueError(f"Unexpected error creating class: {str(e)}")

async def get_classes(db: AsyncSession) -> List[Class]:
    """
    Fetch all classes from the database.
    Returns a list of Class objects.
    Raises ValueError on database errors.
    """
    try:
        result = await db.execute(select(Class))
        return result.scalars().all()
    except SQLAlchemyError as e:
        raise ValueError(f"Error fetching classes: {str(e)}")
    except Exception as e:
        raise ValueError(f"Unexpected error fetching classes: {str(e)}")
