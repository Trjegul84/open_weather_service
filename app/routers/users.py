from datetime import datetime
from typing import List
from itertools import chain

from beanie.odm.fields import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from app.models import  User, UserSchema


router = APIRouter()


class UserCreatedResponse(BaseModel):
    user_id: str


@router.post("/users/register", status_code=status.HTTP_201_CREATED, tags=["Users"])
async def register_user(user: UserSchema):
    user = User(**user.model_dump())
    await user.save()
    return UserCreatedResponse(user_id=str(user.id))
