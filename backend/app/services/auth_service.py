from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy import select
from app.models.user import User
from app.core.security import hash_password, verify_password
from app.schemas.user import UserCreate
import random
import string
from pydantic import EmailStr


async def create_user(db: AsyncSession, user_data: UserCreate) -> User:
    """
    Creates a new user with hashed password and robust validation.
    Raises ValueError on errors (e.g., duplicate username, invalid input).
    """
    try:
        # Validate input fields
        if not user_data.username or not isinstance(user_data.username, str):
            raise ValueError("A valid username is required.")
        if not user_data.email:
            raise ValueError("A valid email is required.")
        allowed_roles = {"ADMIN", "TEACHER", "STUDENT"}
        if user_data.role not in allowed_roles:
            raise ValueError("Role must be ADMIN, TEACHER, or STUDENT")

        # Check for duplicate username/email (early feedback)
        stmt = select(User).where(User.username == user_data.username)
        result = await db.execute(stmt)
        if result.scalars().first():
            raise ValueError("Username already exists")
        stmt = select(User).where(User.email == user_data.email)
        result = await db.execute(stmt)
        if result.scalars().first():
            raise ValueError("Email already exists")

        # Auto-generate password: at least 10 chars, starts with RPS-
        random_part = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        generated_password = f"RPS-{random_part}"
        if len(generated_password) < 10:
            generated_password += ''.join(random.choices(string.ascii_letters + string.digits, k=10-len(generated_password)))

        hashed_password = hash_password(generated_password)

        from app.services.id_utils import generate_rps_id
        user_id = await generate_rps_id(db, User, length=5)
        user = User(
            id=user_id,
            username=user_data.username,
            password_hash=hashed_password,
            role=user_data.role,
            email=user_data.email
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        # Attach generated password for return (not stored in DB)
        user.generated_password = generated_password
        return user
    except IntegrityError as e:
        await db.rollback()
        if "username" in str(e):
            raise ValueError("Username already exists")
        if "email" in str(e):
            raise ValueError("Email already exists")
        raise ValueError(f"Database integrity error: {str(e)}")
    except SQLAlchemyError as e:
        await db.rollback()
        raise ValueError(f"Database error while creating user: {str(e)}")
    except Exception as e:
        await db.rollback()
        raise ValueError(f"Unexpected error creating user: {str(e)}")


async def authenticate_user(db: AsyncSession, username: str, password: str) -> User | None:
    """
    Authenticates a user by username and password.
    Returns the user object if valid, None otherwise.
    Raises ValueError on DB errors.
    """
    try:
        # Query user by username (async-safe)
        stmt = select(User).where(User.username == username).limit(1)
        result = await db.execute(stmt)
        user = result.scalars().first()
        # Check if user exists and password matches
        if user and verify_password(password, user.password_hash):
            return user
        return None  # Invalid credentials
    except SQLAlchemyError as e:
        raise ValueError(f"Database error during authentication: {str(e)}")
    except Exception as e:
        raise ValueError(f"Unexpected error during authentication: {str(e)}")


async def get_user_by_username(db: AsyncSession, username: str) -> User | None:
    """
    Retrieves a user by username (helper for other services).
    Raises ValueError on errors.
    """
    try:
        stmt = select(User).where(User.username == username).limit(1)
        result = await db.execute(stmt)
        user = result.scalars().first()
        return user
    except SQLAlchemyError as e:
        raise ValueError(f"Database error retrieving user: {str(e)}")
    except Exception as e:
        raise ValueError(f"Unexpected error retrieving user: {str(e)}")