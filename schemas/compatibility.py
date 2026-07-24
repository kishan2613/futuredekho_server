from pydantic import BaseModel


class NameCompatibilityRequest(BaseModel):
    name1: str
    name2: str