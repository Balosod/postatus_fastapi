from fastapi import APIRouter, Depends,Response,status
from fastapi_jwt_auth import AuthJWT
from server.models.user import User
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


async def get_user(ID):
    user = await User.get(ID)
    return user

@router.get("/all-coordinates/{latitude}/{longitude}",status_code =200)
async def get_All_coordinate(latitude:float,longitude:float,Authorize: AuthJWT = Depends()):
    
    Authorize.jwt_required()
    
    all_coordinate_list = []
    
    address = get_location(latitude,longitude)
    try:
        city = address["city"]
        pattern = rf'.*{city}.*' 
    except:
        state = address["state"]
        pattern = rf'.*{state}.*'
    
    try:
        products = await Product.find(RegEx(Product.location, pattern,"i"),fetch_links=True).to_list()
        for product in products:
            coordinate_dict ={}
            user = await get_user(product.owner_id)
            try:
                coordinate =  user.coordinates.split(",")
                latitude = coordinate[0]
                longitude = coordinate[1]
                coordinate_dict["latitude"] = latitude
                coordinate_dict["longitude"] = longitude
                coordinate_dict["types"] = product.types
                coordinate_dict["image"] = product.image[0].img
                all_coordinate_list.append(coordinate_dict)
            except:
                pass
    except:
        pass
    
    try:
        services = await Service.find(RegEx(Service.location, pattern,"i"),fetch_links=True).to_list()
        for service in services:
            coordinate_dict ={}
            user = await get_user(service.owner_id)
            try:
                coordinate =  user.coordinates.split(",")
                latitude = coordinate[0]
                longitude = coordinate[1]
                coordinate_dict["latitude"] = latitude
                coordinate_dict["longitude"] = longitude
                coordinate_dict["types"] = service.types
                coordinate_dict["image"] = service.image[0].img
                all_coordinate_list.append(coordinate_dict)
            except:
                pass
    except:
        pass
     
    try:   
        events = await Event.find(RegEx(Event.location, pattern,"i"),fetch_links=True).to_list()
        for event in events:
            coordinate_dict ={}
            user = await get_user(event.owner_id)
            try:
                coordinate =  user.coordinates.split(",")
                latitude = coordinate[0]
                longitude = coordinate[1]
                coordinate_dict["latitude"] = latitude
                coordinate_dict["longitude"] = longitude
                coordinate_dict["types"] = event.types
                coordinate_dict["image"] = event.image[0].img
                all_coordinate_list.append(coordinate_dict)
            except:
                pass
    except:
        pass
    
    try:    
        deliverys = await Delivery.find(RegEx(Delivery.pick_up_location, pattern,"i"),fetch_links=True).to_list()
        for delivery in deliverys:
            coordinate_dict ={}
            user = await get_user(delivery.owner_id)
            try:
                coordinate =  user.coordinates.split(",")
                latitude = coordinate[0]
                longitude = coordinate[1]
                coordinate_dict["latitude"] = latitude
                coordinate_dict["longitude"] = longitude
                coordinate_dict["types"] = delivery.types
                coordinate_dict["image"] = delivery.image[0].img
                all_coordinate_list.append(coordinate_dict)
            except:
                pass
    except:
        pass
        
    return all_coordinate_list

