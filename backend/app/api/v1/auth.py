from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.services.auth_service import authenticate_user, create_user
from app.schemas.user import UserCreate, UserResponse
from app.schemas.auth import Token
from pydantic import BaseModel

# Define a dedicated login schema
class LoginRequest(BaseModel):
    username: str
    password: str
from app.core.security import create_access_token
from app.core.dependencies import require_roles
from sqlalchemy import select, func
from app.models.user import User
from fastapi import Request

router = APIRouter()


@router.post("/login", response_model=Token)
async def login(login_data: LoginRequest, db: AsyncSession = Depends(get_db)):
    """
    User login endpoint. Accepts username and password, returns JWT token if valid.
    """
    user = await authenticate_user(db, login_data.username, login_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.username, "role": user.role.value})
    return {"access_token": access_token}




@router.post("/register")
async def register(user_data: UserCreate, request: Request, db: AsyncSession = Depends(get_db)):
    # Check if username or email already exists
    existing_user = await db.execute(select(User).where(User.username == user_data.username))
    if existing_user.scalar():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
    existing_email = await db.execute(select(User).where(User.email == user_data.email))
    if existing_email.scalar():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")

    # Check if any users exist
    result = await db.execute(select(func.count()).select_from(User))
    user_count = result.scalar()
    user_exists = user_count > 0
    if user_exists:
        # Only require admin if users exist
        from app.core.dependencies import require_roles, get_token_from_header
        try:
            token = get_token_from_header(request)
            await require_roles(["ADMIN", "admin"])(token)
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)
    try:
        user = await create_user(db, user_data)
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role.value if hasattr(user.role, 'value') else user.role,
            "is_active": user.is_active,
            "generated_password": getattr(user, 'generated_password', None)
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Registration failed")