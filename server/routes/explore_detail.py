from fastapi import APIRouter, Depends,status, Response
from fastapi_jwt_auth import AuthJWT
from beanie import PydanticObjectId
from server.models.user import User
from beanie.operators import RegEx,And,Or,In
from server.models.services import (Product, Service, Event, Delivery)


#Authorize: AuthJWT = Depends()
#Authorize.jwt_required()
router = APIRouter()


async def get_similar_item(name,ID):
    
    # get the first three letters of the input name
    
    extracted_name = "".join(name.split()[0][0:3])
    #extracted_name = name
    print(extracted_name)
    pattern = rf'.*{extracted_name}.*'

    
    product = await Product.find(And((RegEx(Product.what_to_sell, pattern,"i")),(Product.id != ID)),fetch_links=True).to_list()
    if product:
        return product
    service = await Service.find(And((RegEx(Service.what_to_do, pattern,"i")),(Service.id != ID)),fetch_links=True).to_list()
    if service:
        return service
    event = await Event.find(And((RegEx(Event.what_is_it_about, pattern,"i")),(Event.id != ID)),fetch_links=True).to_list()
    if event:
        return event
    delivery = await Delivery.find(And((RegEx(Delivery.pick_up_location, pattern,"i")),(Delivery.id != ID)),fetch_links=True).to_list()
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
        context["product"] = product
        searching_name = product.what_to_sell
        product_id = product.id
        user_data = await get_user(product.owner_id)
        context["organizer's info"] = user_data
        item = await get_similar_item(searching_name,product_id)
        if item:
            context["similar_product"] = item
    
        
    service = await Service.find_one(Service.id==ID, fetch_links=True)
    if service:
        context["service"] = service
        searching_name = service.what_to_do
        service_id = service.id
        user_data = await get_user(service.owner_id)
        context["organizer's info"] = user_data
        item = await get_similar_item(searching_name,service_id)
        if item:
            context["similar_service"] = item
        
    event = await Event.find_one(Event.id==ID, fetch_links=True)
    if event:
        context["event"] = event
        searching_name = event.what_is_it_about
        event_id = event.id
        user_data = await get_user(event.owner_id)
        context["organizer's info"] = user_data
        item = await get_similar_item(searching_name,event_id)
        if item:
            context["similar_event"] = item
    
        
    delivery = await Delivery.find_one(Delivery.id==ID, fetch_links=True)
    if delivery:
        context["delivery"] = delivery
        searching_name = delivery.pick_up_location
        delivery_id = delivery.id
        user_data = await get_user(delivery.owner_id)
        context["organizer's info"] = user_data
        item = await get_similar_item(searching_name,delivery_id)
        if item:
            context["similar_delivery"] = item
        
    return context
