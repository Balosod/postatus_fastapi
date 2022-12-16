from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional
from beanie import Document
from pydantic import BaseModel, EmailStr, Field,validator

    
class User(Document):
    email: EmailStr
    password: str
    interest: Optional[list] = None
    active: bool = False
    
    @validator('password', always=True)
    def validate_password(cls, password):
        print("this is password",password)
        min_length = 8
        errors = ''
        if len(password) < min_length:
            errors += 'Password must be at least 8 characters long. '
        if not any(character.islower() for character in password):
            errors += 'Password should contain at least one lowercase character.'
        if errors:
            raise ValueError(errors) 
        return password
    

    class Settings:
        name = "users"

    class Config:
        schema_extra = {
            "example" : {
                "email": "johndoe@mail.com",
                "password": "secretpass123",
            }
        }

class UserCreation(BaseModel):
    email: EmailStr
    password: str
    interest: Optional[list] = None
  

    
        
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

class OtpSchema(BaseModel):
    email: EmailStr = Field(...)
    otp: str = Field(...)
    
class EmailSchema(BaseModel):
    email: EmailStr = Field(...)


def SuccessResponseModel(data, code, message):
    return { "data": [data], "code": code, "message": message }


def ErrorResponseModel(error, code, message):
    return { "error": error, "code": code, "message": message }