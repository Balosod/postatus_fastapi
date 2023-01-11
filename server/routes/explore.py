from fastapi import APIRouter, Depends,Response,status
from fastapi_jwt_auth import AuthJWT
from server.models.services import (Product, Service, Event, Delivery,ExploreSearch)
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
    
    all_explore = []
    all_explore.extend(product)
    all_explore.extend(service)
    all_explore.extend(event)
    all_explore.extend(delivery)
    
    
    return all_explore
    



# @router.get("/lat-long/{latitude}/{longitude}",status_code =200)
# async def explore_by_coordinate(latitude:float,longitude:float, Authorize: AuthJWT = Depends()) -> dict:
    
#     Authorize.jwt_required()
    
#     address = get_location(latitude,longitude)
#     try:
#         city = address["city"]
#         pattern = rf'.*{city}.*' 
#     except:
#         state = address["state"]
#         pattern = rf'.*{state}.*' 
         
#     product = await Product.find(RegEx(Product.location, pattern,"i"),fetch_links=True).to_list()
#     service = await Service.find(RegEx(Service.location, pattern,"i"),fetch_links=True).to_list()      
#     event = await Event.find(RegEx(Event.location, pattern,"i"),fetch_links=True).to_list()      
#     delivery = await Delivery.find(RegEx(Delivery.pick_up_location, pattern,"i"),fetch_links=True).to_list()    
              
#     return {"product":product,"service":service,"event":event,"delivery":delivery}



@router.post("/search",status_code =200)
async def explore_by_search_and_location(search_input:ExploreSearch, Authorize: AuthJWT = Depends()) -> dict:
    Authorize.jwt_required()
   

    search_pattern = rf'{search_input.search}'
    
        
    location_pattern = rf'.*{search_input.location}.*' 
        
    
    product = await Product.find(And(RegEx(Product.title, search_pattern,"i"),RegEx(Product.location, location_pattern,"i")),fetch_links=True).to_list()
    service = await Service.find(And(RegEx(Service.title, search_pattern,"i"),RegEx(Service.location, location_pattern,"i")),fetch_links=True).to_list()      
    event = await Event.find(And(RegEx(Event.title, search_pattern,"i"),RegEx(Event.location, location_pattern,"i")),fetch_links=True).to_list()      
    delivery = await Delivery.find(And(RegEx(Delivery.title, search_pattern,"i"),RegEx(Delivery.pick_up_location, location_pattern,"i")),fetch_links=True).to_list()  
    
    explore_by_search = []
    explore_by_search.extend(product)
    explore_by_search.extend(service)
    explore_by_search.extend(event)
    explore_by_search.extend(delivery)  
              
    return explore_by_search
