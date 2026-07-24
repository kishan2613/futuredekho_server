from fastapi import APIRouter

from schemas.compatibility import (
    NameCompatibilityRequest
)

from services.compatibility_service import (
    generate_name_compatibility
)

router = APIRouter(
    prefix="/compatibility",
    tags=["Compatibility"]
)


@router.post("/name")
async def name_compatibility(
    request: NameCompatibilityRequest
):

    report = generate_name_compatibility(
        request.name1,
        request.name2
    )

    return {
        "success": True,
        "data": report
    }