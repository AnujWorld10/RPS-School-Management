from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.class_ import ClassCreate, ClassResponse
from app.services.class_service import create_class, get_classes
from app.core.dependencies import get_db

router = APIRouter(tags=["Classes"])

@router.post("/", response_model=ClassResponse)
async def add_class(class_data: ClassCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await create_class(db, class_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[ClassResponse])
async def list_classes(db: AsyncSession = Depends(get_db)):
    try:
        return await get_classes(db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
