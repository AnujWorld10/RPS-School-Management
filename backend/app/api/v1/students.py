from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.services.student_service import create_student, get_students, get_student_by_id
from app.schemas.student import StudentCreate, StudentResponse
from app.core.dependencies import require_roles

router = APIRouter()

@router.post("/", response_model=StudentResponse)
async def add_student(student_data: StudentCreate, db: AsyncSession = Depends(get_db), current_user = Depends(require_roles(["ADMIN", "TEACHER"]))):
    try:
        student = await create_student(db, student_data)
        return StudentResponse(id=student.id, name=student.name, roll_number=student.roll_number, class_name=student.class_.name)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/")
async def list_students(db: AsyncSession = Depends(get_db), current_user = Depends(require_roles(["ADMIN", "TEACHER"]))):
    try:
        students = await get_students(db)
        return [StudentResponse(id=s.id, name=s.name, roll_number=s.roll_number, class_name=s.class_.name) for s in students]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))