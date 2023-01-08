from fastapi import APIRouter, Depends,status,Response
from fastapi_jwt_auth import AuthJWT
from server.models.user import User
from server.models.services import (Product, Service, Event, Delivery)
from beanie.operators import RegEx,And,Or
from server.models.order_history import Order
router = APIRouter()



async def get_total_product(ID):
    
    total_sales = 0
    product = await Product.find(Product.owner_id == ID, fetch_links=True).to_list()
    service = await Service.find(Service.owner_id == ID, fetch_links=True).to_list()
    event = await Event.find(Event.owner_id == ID, fetch_links=True).to_list()
    delivery = await Delivery.find(Delivery.owner_id == ID, fetch_links=True).to_list()
    
    order = await Order.find_all().to_list()
    for item in order:
        product = await Product.find(And((Product.id == item.order_id),(Product.owner_id == ID)), fetch_links=True).to_list()
        if product:
            total_sales+=len(product)
        service = await Service.find(And((Service.id == item.order_id),(Service.owner_id == ID)), fetch_links=True).to_list()
        if service:
            total_sales+=len(service)
        event = await Event.find(And((Event.id == item.order_id),(Event.owner_id == ID)), fetch_links=True).to_list()
        if event:
            total_sales+=len(event)
        delivery = await Delivery.find(And((Delivery.id == item.order_id),(Delivery.owner_id == ID)), fetch_links=True).to_list()
        if delivery:
            total_sales+=len(delivery)
    
    
    
    total_products = 0
    total_products+=len(product)
    total_products+=len(service)
    total_products+=len(event)
    total_products+=len(delivery)
    
    return {"total_sales":total_sales,"total_products":total_products,"product":product,"service":service,"event":event,"delivery":delivery}

@router.get("/all",status_code = 200)
async def dashboard(Authorize: AuthJWT = Depends()) -> dict:
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    
    user = await User.find_one(User.email == current_user)
    print(user)
    
    return await get_total_product(user.id)
    


@router.get("/search/{search}",status_code = 200)
async def dashboard_by_tag(search:str,Authorize: AuthJWT = Depends()) -> dict:
    #product = await Product.find(Or(RegEx(Product.location, pattern,"i"),(Product.price == 500)),fetch_links=True).to_list()
    
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    
    user = await User.find_one(User.email == current_user)
    pattern = rf'{search}' 
    product = await Product.find(And(RegEx(Product.what_to_sell, pattern,"i"),(Product.owner_id == user.id)),fetch_links=True).to_list()
    service = await Service.find(And(RegEx(Service.what_to_do, pattern,"i"),(Service.owner_id == user.id)),fetch_links=True).to_list()   
    event = await Event.find(And(RegEx(Event.what_is_it_about, pattern,"i"),(Event.owner_id == user.id)),fetch_links=True).to_list()
    delivery = await Delivery.find(And(RegEx(Delivery.pick_up_location, pattern,"i"),(Delivery.owner_id == user.id)),fetch_links=True).to_list()
          
    result = await get_total_product(user.id)
    total_product = result["total_products"]
    total_sales = result["total_sales"]
        
    return {"total_sales":total_sales,"total_products":total_product, "product":product,"service":service,"event":event,"delivery":delivery}