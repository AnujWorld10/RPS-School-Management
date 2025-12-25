from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.attendance import Attendance
from app.schemas.attendance import AttendanceResponse
from app.core.dependencies import get_db

router = APIRouter()

@router.get("/{attendance_id}", response_model=AttendanceResponse)
async def get_attendance_by_id(attendance_id: str, db: AsyncSession = Depends(get_db)):
    attendance = await db.get(Attendance, attendance_id)
    if not attendance:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    return attendance
