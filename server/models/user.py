from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional
from beanie import Document
from pydantic import BaseModel, EmailStr, Field


class User(Document):
    email: EmailStr
    password: str
    active: bool = True
    is_admin: bool = False
    joined: datetime = datetime.now()

    class Settings:
        name = "users"

    class Config:
        schema_extra = {
            "example" : {
                "email": "johndoe@mail.com",
                "password": "secretpass123",
            }
        }


class UserLogin(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example" : {
                "email": "johndoe@mail.com",
                "password": "yoursecretpa55word",
            }
        }



def SuccessResponseModel(data, code, message):
    return { "data": [data], "code": code, "message": message }


def ErrorResponseModel(error, code, message):
    return { "error": error, "code": code, "message": message }