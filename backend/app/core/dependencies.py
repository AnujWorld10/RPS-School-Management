from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from app.core.config import settings
from app.models.role import RoleEnum

from fastapi import Request

def get_token_from_header(request: Request) -> str:
    auth: str = request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Authorization header"
        )
    return auth.split(" ", 1)[1]

def require_roles(roles: list[RoleEnum]):
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
