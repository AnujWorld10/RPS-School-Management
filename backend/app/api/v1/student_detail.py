from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.student import Student
from app.schemas.student import StudentResponse
from app.core.dependencies import get_db

router = APIRouter()

@router.get("/{student_id}", response_model=StudentResponse)
async def get_student_by_id(student_id: str, db: AsyncSession = Depends(get_db)):
    student = await db.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student
