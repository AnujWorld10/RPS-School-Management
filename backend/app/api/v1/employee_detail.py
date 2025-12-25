from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.employee import Employee
from app.schemas.employee import EmployeeResponse
from app.core.dependencies import get_db

router = APIRouter()

@router.get("/{employee_id}", response_model=EmployeeResponse)
async def get_employee_by_id(employee_id: str, db: AsyncSession = Depends(get_db)):
    employee = await db.get(Employee, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee
