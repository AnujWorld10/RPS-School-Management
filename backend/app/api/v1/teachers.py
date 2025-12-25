from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.services.teacher_service import create_teacher, get_teachers
from app.schemas.teacher import TeacherCreate, TeacherResponse
from app.core.dependencies import require_roles
from app.models.teacher import Teacher

router = APIRouter()

@router.post("/", response_model=TeacherResponse)
async def add_teacher(teacher_data: TeacherCreate, db: AsyncSession = Depends(get_db), current_user = Depends(require_roles(["ADMIN"]))):
    try:
        teacher = await create_teacher(db, teacher_data)
        return TeacherResponse(id=teacher.id, name=teacher.name, subject=teacher.subject.name)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/")
async def list_teachers(db: AsyncSession = Depends(get_db), current_user = Depends(require_roles(["ADMIN"]))):
    try:
        teachers = await get_teachers(db)
        return [TeacherResponse(id=t.id, name=t.name, subject=t.subject.name) for t in teachers]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/{teacher_id}", response_model=TeacherResponse)
async def get_teacher_by_id(teacher_id: str, db: AsyncSession = Depends(get_db)):
    teacher = await db.get(Teacher, teacher_id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return teacher