from fastapi import APIRouter, Depends,Response,status
from fastapi_jwt_auth import AuthJWT
from server.models.services import (Product, Service, Event, Delivery)
from beanie.operators import RegEx,And,Or
from ..utils.location_manager import get_location
import json
router = APIRouter()

@router.get("/all",status_code =200)
async def get_all_explore(Authorize: AuthJWT = Depends()) -> dict:
    
    Authorize.jwt_required()
    
    product = await Product.find(fetch_links=True).to_list()
    service = await Service.find(fetch_links=True).to_list()
    event = await Event.find(fetch_links=True).to_list()
    delivery = await Delivery.find(fetch_links=True).to_list()
    
    all_service_list = []
    all_service_list.extend(product)
    all_service_list.extend(service)
    all_service_list.extend(event)
    all_service_list.extend(delivery)
    
    
    return all_service_list
    



@router.get("/lat-long/{latitude}/{longitude}",status_code =200)
async def explore_by_coordinate(latitude:float,longitude:float, Authorize: AuthJWT = Depends()) -> dict:
    
    Authorize.jwt_required()
    
    address = get_location(latitude,longitude)
    try:
        city = address["city"]
        pattern = rf'.*{city}.*' 
    except:
        state = address["state"]
        pattern = rf'.*{state}.*' 
         
    product = await Product.find(RegEx(Product.location, pattern,"i"),fetch_links=True).to_list()
    service = await Service.find(RegEx(Service.location, pattern,"i"),fetch_links=True).to_list()      
    event = await Event.find(RegEx(Event.location, pattern,"i"),fetch_links=True).to_list()      
    delivery = await Delivery.find(RegEx(Delivery.pick_up_location, pattern,"i"),fetch_links=True).to_list()    
              
    return {"product":product,"service":service,"event":event,"delivery":delivery}



@router.get("/tag-loc/{tag}/{location}",status_code =200)
async def explore_by_tag_and_location(tag:str,location:str, Authorize: AuthJWT = Depends()) -> dict:
    
    Authorize.jwt_required()
    
    tag_pattern = rf'{tag}'
    location_pattern = rf'.*{location}.*' 
    
    product = await Product.find(And(RegEx(Product.tags, tag_pattern,"i"),RegEx(Product.location, location_pattern,"i")),fetch_links=True).to_list()
    service = await Service.find(And(RegEx(Service.tags, tag_pattern,"i"),RegEx(Service.location, location_pattern,"i")),fetch_links=True).to_list()      
    event = await Event.find(And(RegEx(Event.tags, tag_pattern,"i"),RegEx(Event.location, location_pattern,"i")),fetch_links=True).to_list()      
    delivery = await Delivery.find(And(RegEx(Delivery.tags, tag_pattern,"i"),RegEx(Delivery.pick_up_location, location_pattern,"i")),fetch_links=True).to_list()    
              
    return {"product":product,"service":service,"event":event,"delivery":delivery}
