from typing import Optional, List

from beanie import Document, Link
from beanie.odm.fields import PydanticObjectId

from pydantic import BaseModel


class UserSchema(BaseModel):
    username: Optional[str]


class User(Document):
    pass


class UserId(BaseModel):
    id: PydanticObjectId


class WeatherDataModel(BaseModel):
    city_id: int
    temperature: float
    humidity: float


class WeatherDataSchema(BaseModel):
    timestamp: str
    user: Link[User]


class WeatherData(WeatherDataSchema, Document):
    wdata: Optional[List[WeatherDataModel]] = []
