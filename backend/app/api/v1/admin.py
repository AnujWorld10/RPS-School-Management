from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.models.fee import Fee
from app.schemas.fee import FeeCreate
from app.core.dependencies import require_roles

router = APIRouter()

@router.post("/fees")
async def add_fee(fee_data: FeeCreate, db: AsyncSession = Depends(get_db), current_user = Depends(require_roles(["ADMIN"]))):
    try:
        fee = Fee(**fee_data.dict())
        db.add(fee)
        await db.commit()
        return {"message": "Fee added"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))