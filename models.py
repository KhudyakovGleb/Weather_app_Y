from datetime import date, timedelta
from pydantic import BaseModel, Field, validator
import re
from uuid import UUID, uuid4


class AppInfo(BaseModel):
    version: str = "0.1.0"
    service: str = "weather"
    author: str = "KhudyakovGleb"


class WeatherTempStorage(BaseModel):
    id: UUID = uuid4()
    geo_place: str = "Russia, Saint-Petersburg"
    date_start: date = Field(default_factory=lambda: date.today() - timedelta(days=1))
    date_end: date = Field(default_factory=date.today)
    temp_value: list
    median_value: float
    avg_value: float
    min_value: float
    max_value: float

    @validator("date_start", "date_end", pre=True)
    def validate_date_format(cls, value):
        if isinstance(value, str):
            if not re.match(r"^\d{4}-\d{2}-\d{2}$", value):
                raise ValueError("Date must be in YYYY-MM-DD format.")
            return date.fromisoformat(value)
        return value
