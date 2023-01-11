from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional
from beanie import Document
from pydantic import BaseModel, EmailStr, Field,validator
from enum import Enum
from beanie import PydanticObjectId


class AccountType(str,Enum):
    VENDOR = "VENDOR"
    NONE_VENDOR = "NONE_VENDOR"
    
class User(Document):
    email: EmailStr
    firstname:Optional[str] = None
    lastname:Optional[str] = None
    about:Optional[str] = None
    address:Optional[str] = None
    coordinates:Optional[str] = None
    password: str
    interest: Optional[list] = None
    provider:str = "Normal Registration"
    img:Optional[str] = None
    account_type:Optional[AccountType] = AccountType.VENDOR
    my_order:Optional[int] = 0
    active: bool = False
    
    @validator('password', always=True)
    def validate_password(cls, password):
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
    firstname:Optional[str] = None
    lastname:Optional[str] = None
    about:Optional[str] = None
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


class ImageSchema(BaseModel):
    image: str
    

class InterestSchema(BaseModel):
    interest: list
    
class DeleteUser(BaseModel):
    email: EmailStr = Field(...)
    

def SuccessResponseModel(data, code, message):
    return { "data": [data], "code": code, "message": message }


def ErrorResponseModel(error, code, message):
    return { "error": error, "code": code, "message": message }