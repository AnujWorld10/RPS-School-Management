
"""
Dependency utilities for FastAPI routes: DB session, JWT auth, and role-based access.
"""
from app.database.session import async_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status, Request
from jose import jwt, JWTError
from app.core.config import settings
from app.models.role import RoleEnum

async def get_db() -> AsyncSession:
    """Yield an async SQLAlchemy session for DB operations."""
    async with async_session() as session:
        yield session

def get_token_from_header(request: Request) -> str:
    """Extract Bearer token from Authorization header, or raise 401."""
    auth: str = request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Authorization header"
        )
    return auth.split(" ", 1)[1]

def require_roles(roles: list[RoleEnum]):
    """Dependency: require JWT with one of the specified roles."""
    def role_checker(token: str = Depends(get_token_from_header)):
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            if payload.get("role") not in roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions"
                )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
    return role_checker
