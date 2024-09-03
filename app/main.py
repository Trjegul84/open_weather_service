from beanie import init_beanie
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi_lifespan_manager import LifespanManager
from motor.motor_asyncio import AsyncIOMotorClient

from app.models import User, WeatherData
from app.routers import data, users
from app.settings import Settings


settings = Settings()

lifespan = LifespanManager()

description = """
Service connected with Open Weather API to collect weather data of cities

## Users

You can register a user and get a unique user id

## Weather

You will be able to:

* Make post request to retrieve weather data of a list of countries
* Get the progress percentage of the current post request
"""

@lifespan.add
async def init_db(app: FastAPI):
    client = AsyncIOMotorClient(settings.DB_URL)
    await init_beanie(database=client[settings.DB_NAME], document_models=[User, WeatherData])
    yield


app = FastAPI(
    lifespan=lifespan,
    title="Open Weather API Service",
    description=description,
    summary="Using FastAPI, MongoDB and Docker",
    version="1.0.0",
    contact={
        "name": "Angela Checa",
        "email": "angelachek@gmail.com",
    },
)

app.include_router(users.router)
app.include_router(data.router)


@app.get("/", include_in_schema=False)
def redirect_root():
    return RedirectResponse(url='/docs')
