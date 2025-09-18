from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class WeatherRecord(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    city: str = Field(index=True)
    latitude: float
    longitude: float
    temperature: float
    windspeed: float
    observed_at: datetime = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
