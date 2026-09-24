from pydantic import BaseModel


class KundliRequest(BaseModel):
    name: str
    date: str
    time: str
    latitude: float
    longitude: float
    timezone: float