from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, Depends
from passlib.context import CryptContext
from typing import List

# from auth.auth_handler import signJWT
from fastapi_jwt_auth import AuthJWT


from server.models.user import (
    User,
    UserLogin,
    SuccessResponseModel,
    ErrorResponseModel
)
from server.models.review import ProductReview



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter()


@router.post("/", response_description="User added to the database")
async def create_account(user: User) -> dict:
    user_exists = await User.find_one(User.email == user.email)

    if user_exists:
        return HTTPException(
            status_code=400,
            detail="Email already exists!"
        )

    user.password = pwd_context.hash(user.password)
    await user.create()   
    # signJWT(user.email) 
    return SuccessResponseModel(user, 201, "Account successfully created!" )


@router.get("/", response_description="List users on the database")
async def list_all_users() -> List[User]:
    users = await User.find_all().to_list()
    return SuccessResponseModel(users, 200, "Account successfully created!" )


@router.get("/{id}", response_description="List users on the database")
async def list_all_users(id: PydanticObjectId) -> User:
    user = await User.get(id)
    return SuccessResponseModel(user, 200, "Account successfully created!" )


@router.post("/login", response_description="User login")
async def login_user(user: UserLogin, Authorize: AuthJWT = Depends()):
    user_acct = await User.find_one(User.email == user.email)

    if user_acct and pwd_context.verify(user.password, user_acct.password):
        access_token = Authorize.create_access_token(subject=user.email)
        refresh_token = Authorize.create_refresh_token(subject=user.email)
        return {"access_token": access_token, "refresh_token": refresh_token}
        # return signJWT(user_acct.email)

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