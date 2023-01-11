from fastapi import APIRouter, Depends,status, Response
from fastapi_jwt_auth import AuthJWT
from beanie import PydanticObjectId
from server.models.user import User
from beanie.operators import RegEx,And,Or,In
from server.models.services import (Product, Service, Event, Delivery)
import json
from pydantic import BaseModel


#Authorize: AuthJWT = Depends()
#Authorize.jwt_required()
router = APIRouter()


async def get_similar_item(name,ID):
    
    # get the first three letters of the input name
    
    extracted_name = "".join(name.split()[0][0:3])
    print(extracted_name)
    pattern = rf'.*{extracted_name}.*'

    
    product = await Product.find(And((RegEx(Product.title, pattern,"i")),(Product.id != ID)),fetch_links=True).to_list()
    if product:
        return product
    service = await Service.find(And((RegEx(Service.title, pattern,"i")),(Service.id != ID)),fetch_links=True).to_list()
    if service:
        return service
    event = await Event.find(And((RegEx(Event.title, pattern,"i")),(Event.id != ID)),fetch_links=True).to_list()
    if event:
        return event
    delivery = await Delivery.find(And((RegEx(Delivery.title, pattern,"i")),(Delivery.id != ID)),fetch_links=True).to_list()
    if delivery:
        return delivery
    else:
        return None

 
async def get_user(ID):
    user = await User.get(ID)
    return user

@router.get("/{ID}",status_code = 200)
async def detail(ID:PydanticObjectId, Authorize: AuthJWT = Depends()) -> dict:
    
    Authorize.jwt_required()
    
    context = {}
    product = await Product.find_one(Product.id==ID, fetch_links=True)
    if product:
        context["detail"] = product
        searching_name = product.title
        product_id = product.id
        user_data = await get_user(product.owner_id)
        context["organizer's_info"] = user_data
        item = await get_similar_item(searching_name,product_id)
        if item:
            context["similar_detail"] = item
    
        
    service = await Service.find_one(Service.id==ID, fetch_links=True)
    if service:
        context["detail"] = service
        searching_name = service.title
        service_id = service.id
        user_data = await get_user(service.owner_id)
        context["organizer's_info"] = user_data
        item = await get_similar_item(searching_name,service_id)
        if item:
            context["similar_detail"] = item
        
    event = await Event.find_one(Event.id==ID, fetch_links=True)
    if event:
        context["detail"] = event
        searching_name = event.title
        event_id = event.id
        user_data = await get_user(event.owner_id)
        context["organizer's_info"] = user_data
        item = await get_similar_item(searching_name,event_id)
        if item:
            context["similar_detail"] = item
    
        
    delivery = await Delivery.find_one(Delivery.id==ID, fetch_links=True)
    if delivery:
        context["detail"] = delivery
        searching_name = delivery.title
        delivery_id = delivery.id
        user_data = await get_user(delivery.owner_id)
        context["organizer's_info"] = user_data
        item = await get_similar_item(searching_name,delivery_id)
        if item:
            context["similar_detail"] = item
        
    return context
