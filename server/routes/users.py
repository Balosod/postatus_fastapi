from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, Depends
from passlib.context import CryptContext
from pydantic import  EmailStr, Field
from typing import List
from ..utils.helpers import fm
from ..utils.helpers import EmailManager
from ..utils import auth_service


# from auth.auth_handler import signJWT
from fastapi_jwt_auth import AuthJWT

from server.models.interest import Interest
from server.models.user import (
    User,
    UserLogin,
    OtpSchema,
    EmailSchema,
    UserCreation,
    SuccessResponseModel,
    ErrorResponseModel
)



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter()


@router.post("/", response_description="User added to the database")
async def create_account(user: UserCreation) -> dict:
    user_interest=[]
    user_exists = await User.find_one(User.email == user.email)

    if user_exists:
        return HTTPException(
            status_code=400,
            detail="Email already exists!"
        )
    try:
        for ID in user.interest:
            interest_name = await Interest.get(ID)
            user_interest.append(interest_name.interest)      
    except:
        pass
        
    hashed_password = pwd_context.hash(user.password)
    user_obj = User(
        email=user.email,
        password=hashed_password,
        interest=user_interest
    )
    await user_obj.create() 
    
    message  = EmailManager.send_welcome_msg(user.email)
    await fm.send_message(message)
    return SuccessResponseModel(user, 201, "Account successfully created!" )



@router.post("/auth/login", response_description="User login")
async def login_user(user: UserLogin, Authorize: AuthJWT = Depends()):
    user_acct = await User.find_one(User.email == user.email)

    if user_acct and user_acct.active and pwd_context.verify(user.password, user_acct.password):
        access_token = Authorize.create_access_token(subject=user.email)
        refresh_token = Authorize.create_refresh_token(subject=user.email)
        return {"access_token": access_token, "refresh_token": refresh_token}

    return HTTPException(
            status_code=300,
            detail="User with that email doesn't exist!"
        )


@router.post("/refresh", response_description="Get new access token")
def get_new_access_token(Authorize: AuthJWT = Depends()):
    Authorize.jwt_refresh_token_required()

    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=current_user)
    return {"access_token": new_access_token}


@router.post("/auth/verify", response_description="verify otp")
async def verify_otp(data: OtpSchema):
    
    obj = await auth_service.verify_OTP(data.email,data.otp)
    return {"message":obj}


@router.post("/auth/resend", response_description="resend otp")
async def resend_otp(data:EmailSchema):

    obj = await auth_service.resend_OTP(data.email)
    return {"message":obj}




# @router.post("/profile", response_description="resend otp")
# async def resend_otp(data:EmailSchema):
#     user_acct = await User.find_one(User.email == data.email)
#     inte = user_acct.interest
#     print(inte)
#     inte.remove("Grocery")
#     print(inte)
#     return user_acct
