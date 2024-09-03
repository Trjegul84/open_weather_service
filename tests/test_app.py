from unittest.mock import ANY

import pytest
from fastapi import FastAPI, status
from fastapi.testclient import TestClient

from app.main import app, lifespan, settings
from app.models import User, WeatherData

settings.DB_NAME = "test"


@lifespan.add
async def empty_db(app: FastAPI):
    await User.find_all().delete()
    await WeatherData.find_all().delete()
    yield


@pytest.fixture
def user(client):
    return create_user(client)


def create_user(client):
    user = dict(username="Bruce Wayne")

    response = client.post("/users/register", json=user)

    assert response.json() == dict(user_id=ANY)
    assert response.status_code == status.HTTP_201_CREATED

    return user | dict(id=response.json()["user_id"])


@pytest.fixture
def client():
    with TestClient(app) as _client:
        yield _client


@pytest.fixture
def non_existing_user_id():
    return "657cb8cf78775fe7635f6fff"


@pytest.fixture
def unique_request_user_id(client):
    user = create_user(client)
    user_id = user["id"]
    return user_id


def save_post_request(client):
    user = create_user(client)
    user_id = user["id"]
    client.post(f"/weather?user_id={user_id}", json="")
    return user_id


def test_register_user(client):
    create_user(client)


def test_collect_data_fails_when_user_does_not_exists(client, non_existing_user_id):
    response = client.post(f"/weather?user_id={non_existing_user_id}", json="")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == dict(detail="User id does not exists.")


def test_collect_data_fails_when_request_user_id_is_not_unique(client):
    non_unique_user_id = save_post_request(client)

    response = client.post(f"/weather?user_id={non_unique_user_id}", json="")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == dict(
        detail="User id was already used for a previous request."
    )


def test_collect_data_responds_ok_when_request_user_id_is_unique(
    client, unique_request_user_id
):

    response = client.post(f"/weather?user_id={unique_request_user_id}", json="")

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == dict(
        message="The current request is in progress, use the GET endpoint to know the status."
    )


def test_get_progress_percentage_fails_when_user_does_not_exists(
    client, non_existing_user_id
):
    response = client.get(f"/weather/{non_existing_user_id}")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == dict(detail="User id does not exists.")


def test_get_progress_percentage_fails_when_user_has_not_made_any_request(
    client, unique_request_user_id
):
    # User is created but no register in WeatherData document is linked to it
    response = client.get(f"/weather/{unique_request_user_id}")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == dict(detail="User has not made any request.")


def test_get_progress_percentage_ok_when_request_user_has_weather_data(client):
    unique_user_id = save_post_request(client)

    response = client.get(f"/weather/{unique_user_id}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == dict(percentage="0.00 %")


def test_homepage_redirects_to_docs(client):
    response = client.get("/")

    assert response.status_code == status.HTTP_200_OK
