import asyncio
from datetime import datetime

import httpx

from beanie.odm.fields import PydanticObjectId
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from app.models import User, WeatherData
from app.secrets import get_secret
from app.settings import cities

router = APIRouter()


class WeatherDataResponse(BaseModel):
    message: str


class PercentageResponse(BaseModel):
    percentage: str


async def get_weather_data(weather_data: WeatherData):
    api_key = (get_secret("open_weather_api"))

    for city_id in cities:
        api_url = f"http://api.openweathermap.org/data/2.5/weather?id={city_id}&units=metric&appid={api_key}"
        async with httpx.AsyncClient() as client:
            response = await client.get(api_url)
            response_data = response.json()
            update_query ={
                "$push":{
                    "wdata": {
                        "city_id": response_data["id"],
                        "temperature": response_data["main"]["temp"],
                        "humidity": response_data["main"]["humidity"]
                    }
                }
            }

            await weather_data.update(update_query)

    return weather_data.wdata


@router.post("/weather", status_code=status.HTTP_201_CREATED, tags=["WeatherData"])
async def collect_weather_data(user_id: PydanticObjectId) -> WeatherDataResponse:
    user = await User.get(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User id does not exists.")
    else:
        previous_user_request = await WeatherData.find_one(WeatherData.user.id == user_id)

        if previous_user_request:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User id was already used for a previous request.")

        weather_data = WeatherData(
            user=user,
            timestamp=str(datetime.now()),
        )
        weather_data = await weather_data.save()
        asyncio.create_task(get_weather_data(weather_data))

        return WeatherDataResponse(message="The current request is in progress, use the GET endpoint to know the status.")


@router.get("/weather/{user_id}", tags=["WeatherData"])
async def get_progress_percentage(user_id: PydanticObjectId) -> PercentageResponse:
    user = await User.get(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User id does not exists.")

    else:
        previous_user_request = await WeatherData.find_one(WeatherData.user.id == user_id)

        if not previous_user_request:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User has not made any request.")

        weather_data = await WeatherData.find(WeatherData.user.id == user_id, fetch_links=True).first_or_none()
        get_percentage = lambda quantity: (quantity*100/(len(cities)))
        percentage = get_percentage(len(weather_data.wdata))

        return PercentageResponse(percentage=f'{percentage:.2f} %')
