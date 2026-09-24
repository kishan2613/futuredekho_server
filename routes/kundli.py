from fastapi import APIRouter, HTTPException

from schemas.kundli import KundliRequest

from services.kundli_service import generate_complete_kundli

router = APIRouter(
    prefix="/kundli",
    tags=["Kundli"]
)


@router.post("/")
async def generate_kundli(data: KundliRequest):

    try:

        result = await generate_complete_kundli(data)

        return {
            "success": True,
            "data": result
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )