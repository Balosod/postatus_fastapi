from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT
from beanie import PydanticObjectId
from server.models.user import User
import base64
import uuid
from server.models.services import (Product, Service, Event, Delivery)


#Authorize: AuthJWT = Depends()
#Authorize.jwt_required()
router = APIRouter()

@router.get("/{ID}")
async def detail(ID:PydanticObjectId) -> dict:
    
        product = await Product.find(Product.id==ID, fetch_links=True).to_list()
        if product:
            return product  
        service = await Service.find(Service.id==ID, fetch_links=True).to_list()
        if service:
            return service
        event = await Event.find(Event.id==ID, fetch_links=True).to_list()
        if event:
            return event
        delivery = await Delivery.find(Delivery.id==ID, fetch_links=True).to_list()
        if delivery:
            return delivery
        else:
            return {"message":"something went wrong"}
