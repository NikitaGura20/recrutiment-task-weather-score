from pydantic import BaseModel


class CityScoreResponse(BaseModel):
    city: str
    country: str
    score: float