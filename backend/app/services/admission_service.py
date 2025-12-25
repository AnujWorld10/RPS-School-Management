
import random
import string
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.models.admission import Admission, AdmissionStatus
from app.schemas.admission import AdmissionCreate
from typing import List

# Helper to generate unique Rps_XXXXXX ID
async def generate_admission_id(db: AsyncSession) -> str:
    while True:
        rand_id = "Rps_" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        exists = await db.get(Admission, rand_id)
        if not exists:
            return rand_id

async def create_admission(db: AsyncSession, admission_data: AdmissionCreate) -> Admission:
    """
    Create a new admission with validation and robust error handling.
    Raises ValueError for validation or DB errors.
    """
    try:
        data = admission_data.dict()
        required_fields = ["student_id", "application_date"]
        for field in required_fields:
            if not data.get(field):
                raise ValueError(f"{field} is required.")
        admission_id = await generate_admission_id(db)
        admission = Admission(admission_id=admission_id, **data)
        db.add(admission)
        await db.commit()
        await db.refresh(admission)
        return admission
    except IntegrityError as e:
        await db.rollback()
        raise ValueError(f"Database integrity error: {str(e)}")
    except SQLAlchemyError as e:
        await db.rollback()
        raise ValueError(f"Database error: {str(e)}")
    except Exception as e:
        await db.rollback()
        raise ValueError(f"Unexpected error creating admission: {str(e)}")
