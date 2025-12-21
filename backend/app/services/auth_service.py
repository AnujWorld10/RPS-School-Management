from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy import select
from app.models.user import User
from app.core.security import hash_password, verify_password
from app.schemas.auth import UserCreate

async def create_user(db: AsyncSession, user_data: UserCreate):
    """
    Creates a new user with hashed password.
    Raises ValueError on errors (e.g., duplicate username).
    """
    try:
        # Validate password byte length for bcrypt (max 72 bytes)
        pw_bytes = user_data.password.encode('utf-8') if isinstance(user_data.password, str) else user_data.password
        if len(pw_bytes) > 72:
            raise ValueError("Password too long: bcrypt supports a maximum of 72 bytes. Shorten the password or truncate to 72 bytes.")

        # Hash the password for security
        hashed_password = hash_password(user_data.password)
        
        # Create user instance
        user = User(
            username=user_data.username,
            password_hash=hashed_password,
            role=user_data.role
        )
        
        # Add to DB and commit
        db.add(user)
        await db.commit()
        await db.refresh(user)  # Refresh to get the ID
        
        return user
    
    except IntegrityError as e:
        # Handle unique constraint violations (e.g., duplicate username)
        await db.rollback()
        if "username" in str(e):
            raise ValueError("Username already exists")
        raise ValueError(f"Database integrity error: {str(e)}")
    
    except SQLAlchemyError as e:
        # General DB errors
        await db.rollback()
        raise ValueError(f"Database error while creating user: {str(e)}")
    
    except Exception as e:
        # Unexpected errors
        await db.rollback()
        raise ValueError(f"Unexpected error creating user: {str(e)}")

async def authenticate_user(db: AsyncSession, username: str, password: str):
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
        # DB query errors
        raise ValueError(f"Database error during authentication: {str(e)}")
    
    except Exception as e:
        # Unexpected errors
        raise ValueError(f"Unexpected error during authentication: {str(e)}")

async def get_user_by_username(db: AsyncSession, username: str):
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