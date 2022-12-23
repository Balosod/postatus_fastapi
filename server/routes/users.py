from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, Depends
from passlib.context import CryptContext
from pydantic import  EmailStr, Field
from typing import List
from ..utils.helpers import fm
from ..utils.helpers import EmailManager
from ..utils import auth_service
import base64
import uuid
from ..utils.s3_storage import client
from ..settings import CONFIG_SETTINGS
from server.models.order_history import Order
from ..utils.location_manager import get_location

# from auth.auth_handler import signJWT
from fastapi_jwt_auth import AuthJWT

from server.models.interest import Interest
from server.models.user import (
    User,
    UserLogin,
    OtpSchema,
    EmailSchema,
    UserCreation,
    ImageSchema,
    InterestSchema,
    AccountType,
    SuccessResponseModel,
    ErrorResponseModel
)



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter()


@router.post("/signup/{latitude}/{longitude}", response_description="User added to the database")
async def create_account(user: UserCreation,latitude:float,longitude:float) -> dict:
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
    
    get_address = get_location(latitude,longitude)
    if get_address:
        try:
            user_address = f"{get_address['city']} {get_address['state']},{get_address['country']}"
            print(user_address)
        except:
           user_address = f"{get_address['state']},{get_address['country']}"
           print(user_address) 
    else:
        user_address = ""
    
    user_coordinates = f"{latitude},{longitude}"
    hashed_password = pwd_context.hash(user.password)
    user_obj = User(
        email=user.email,
        password=hashed_password,
        address = user_address,
        coordinates = user_coordinates,
        interest=user_interest
    )
    await user_obj.create() 
    
    message  = EmailManager.send_welcome_msg(user.email)
    await fm.send_message(message)
    return SuccessResponseModel(user_obj, 201, "Account successfully created!" )



@router.post("/auth/login", response_description="User login")
async def login_user(user: UserLogin, Authorize: AuthJWT = Depends()):
    print("called")
    user_acct = await User.find_one(User.email == user.email)
    print(user)
    try:
        if user_acct and user_acct.active and pwd_context.verify(user.password, user_acct.password):
            access_token = Authorize.create_access_token(subject=user.email)
            refresh_token = Authorize.create_refresh_token(subject=user.email)
            return {"access_token": access_token, "refresh_token": refresh_token}
        return HTTPException(
                status_code=300,
                detail="User with that email doesn't exist!"
            )
    except:
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




@router.post("/profile/image", response_description="Upload profile image")
async def upload_profile_image(data:ImageSchema, Authorize: AuthJWT = Depends()):
    
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    
    user = await User.find_one(User.email == current_user)
    if user:
        if CONFIG_SETTINGS.USE_SPACES:
            img_name = str(uuid.uuid4())[:10] + '.png'
            image_as_bytes = str.encode(data.image) 
            img_recovered = base64.b64decode(image_as_bytes)
            
            client.put_object(
            Bucket=CONFIG_SETTINGS.BUCKET,
            Body=img_recovered,
            Key=f"image/{img_name}",
            ACL=CONFIG_SETTINGS.ACL,
            ContentType="image/png"
            )
                
            img_url = f"https://postatusapistorage.nyc3.digitaloceanspaces.com/image/{img_name}"
            
            user.img = img_url
            await user.save()
            
            return{"message":"image successfully uploaded"}
        else:
            img_name = str(uuid.uuid4())[:10] + '.png'
            image_as_bytes = str.encode(data.image) 
            img_recovered = base64.b64decode(image_as_bytes)
            
            with open("server/media/image/uploaded_" + img_name, "wb") as f:
                f.write(img_recovered)
                
            img_url = f"http://localhost:8000/media/image/uploaded_{img_name}"
            
            user.img = img_url
            await user.save()
            
            return{"message":"image successfully uploaded"}
    else:
        return{"message":"User not found"}
    

@router.get("/profile/account/{acctype}")
async def account_type(acctype:AccountType,Authorize: AuthJWT = Depends()):
     
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    
    user = await User.find_one(User.email == current_user)
    if user:
        user.account_type = acctype
        await user.save()
        return{"message":"account type successfully updated"} 
    else:
        return{"message":"User not found"}
    
    obj = await auth_service.resend_OTP(data.email)
    return {"message":obj}


@router.get("/my/profile")
async def get_profile(Authorize: AuthJWT = Depends()):
     
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    
    user = await User.find_one(User.email == current_user)
    if user:
        return user
    else:
        return{"message":"User not found"}
    

@router.delete("/profile/delete/interest/{data}")
async def delete_interest(data:str, Authorize: AuthJWT = Depends()):
     
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    
    user = await User.find_one(User.email == current_user)
    if user:
        try:
            user.interest.remove(data)
            await user.save()
            return user
        except:
            return {"message":"Interest not found"}
    else:
        return{"message":"User not found"}
    

@router.post("/profile/add/interest/")
async def add_interest(data:InterestSchema, Authorize: AuthJWT = Depends()):
     
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    
    user = await User.find_one(User.email == current_user)
    if user:
        print(user.interest)
        try:
            for ID in data.interest:
                interest_name = await Interest.get(ID)
                user.interest.append(interest_name.interest)   
                await user.save()
                return user   
        except:
            pass
    else:
        return{"message":"User not found"}