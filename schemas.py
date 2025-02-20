from datetime import date, timedelta
from pydantic import BaseModel, Field, validator
import re
from uuid import UUID, uuid4
from typing import Dict


class GetWeatherInsert(BaseModel):
    geo_place: str = "Russia, Saint-Petersburg"
    date_start: date = Field(default_factory=lambda: date.today() - timedelta(days=1))
    date_end: date = Field(default_factory=date.today)

    @validator("date_start", "date_end", pre=True)
    def validate_date_format(cls, value):
        if isinstance(value, str):
            if not re.match(r"^\d{4}-\d{2}-\d{2}$", value):
                raise ValueError("Date must be in YYYY-MM-DD format.")
            return date.fromisoformat(value)
        return value


class GetWeatherOutput(BaseModel):
    average: float
    median: float
    min: float
    max: float


class WeatherResponse(BaseModel):
    data: Dict[str, GetWeatherOutput]
    service: str = "weather"
