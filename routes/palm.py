from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends
)

from utils.file_handler import save_image
from agents.palm import (
    extract_palm_features
)
from database import get_db
from models.palm import Palm
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from utils.cloudinary import upload_image
import json
from sqlalchemy import select
router = APIRouter()


@router.post("/analyze")
async def analyze_palm(
    user_id: UUID,
    image: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):


    filepath = await save_image(image)


    image_url = await upload_image(filepath)


    palm_features = extract_palm_features(filepath)

    cleaned = (
        palm_features
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    palm_data = json.loads(cleaned)

    palm = Palm(
        user_id=user_id,
        image_url=image_url,
        palm_data=palm_data
    )

    db.add(palm)
    await db.commit()

    return {
        "success": True,
        "image_url": image_url,
        "palm_id": str(palm.id)
    }

@router.get("/user/{user_id}")
async def get_user_palms(
    user_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Palm)
        .where(Palm.user_id == user_id)
        .order_by(Palm.id.desc())
    )

    palms = result.scalars().all()

    return {
        "success": True,
        "palms": [
            {
                "id": palm.id,
                "image_url": palm.image_url,
                "palm_data": palm.palm_data
            }
            for palm in palms
        ]
    }