import requests
from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/horoscope",
    tags=["Horoscope"]
)

HOROSCOPE_API = "https://freehoroscopeapi.com/api/v1/get-horoscope/daily"


@router.get("/daily")
async def get_daily_horoscope(sign: str):
    try:
        response = requests.get(
            HOROSCOPE_API,
            params={"sign": sign.lower()},
            timeout=10
        )

        response.raise_for_status()

        return {
            "success": True,
            "data": response.json()
        }

    except requests.RequestException as e:
        raise HTTPException(
            status_code=502,
            detail=f"Horoscope API unavailable: {str(e)}"
        )