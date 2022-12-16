from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT
from server.models.services import (Product, Service, Event, Delivery)

router = APIRouter()

@router.get("/")
async def get_all_explore() -> dict:
    
    product = await Product.find(fetch_links=True).to_list()
    service = await Service.find(fetch_links=True).to_list()
    event = await Event.find(fetch_links=True).to_list()
    delivery = await Delivery.find(fetch_links=True).to_list()
        
    return {"product":product,"service":service,"event":event,"delivery":delivery}


@router.get("/{loc}")
async def explore_by_location() -> dict:
    
    product = await Product.find("osun").to_list()
    
        
    return {"product":product}
