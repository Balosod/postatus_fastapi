from fastapi import APIRouter, Depends,Response, status
from fastapi_jwt_auth import AuthJWT
from server.models.interest import Interest



router = APIRouter()

@router.post("/add", status_code = 201)
async def create_interest(interest:Interest) -> dict:
    
    await interest.create()
    
    return {"message":f"{interest.interest} successfully added to interest list"}


@router.get("/all",status_code =200)
async def get_interest() -> dict:
    all_interest = await Interest.find().to_list()

    return all_interest
