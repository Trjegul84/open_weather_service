from typing import List, Optional

from beanie import Document, Link
from pydantic import BaseModel


class UserSchema(BaseModel):
    username: Optional[str]


class User(Document):
    pass


class WeatherDataModel(BaseModel):
    city_id: int
    temperature: float
    humidity: float


class WeatherDataSchema(BaseModel):
    timestamp: str
    user: Link[User]


class WeatherData(WeatherDataSchema, Document):
    wdata: Optional[List[WeatherDataModel]] = []
