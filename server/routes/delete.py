from fastapi import APIRouter, Depends,status,Response
from fastapi_jwt_auth import AuthJWT
from beanie import PydanticObjectId
from server.models.user import User,DeleteUser
from server.models.services import (Product, Service, Event, Delivery)




router = APIRouter()



@router.delete("/all/product", status_code = 200)
async def delete_all_product(response:Response) -> dict:
    try:
        products = await Product.find(fetch_links=True).to_list()
        for product in products:
            product_to_delete = await Product.get(product.id)
            await product_to_delete.delete()
        return{"message":"all product successfully deleted"}
    except:
        response.status_code = 400
        return {"message":"something went wrong! or empty product list"}  
  
  
    
@router.delete("/all/service", status_code = 200)
async def delete_all_services(response:Response) -> dict:
    try:
        services = await Service.find(fetch_links=True).to_list()
        for service in services:
            service_to_delete = await Service.get(service.id)
            await service_to_delete.delete()
        return{"message":"all service successfully deleted"}
    except:
        response.status_code = 400
        return {"message":"something went wrong! or empty service list"}  
    
    
@router.delete("/all/event", status_code = 200)
async def delete_all_event(response:Response) -> dict:
    try:
        events = await Event.find(fetch_links=True).to_list()
        print(len(events))
        for event in events:
            event_to_delete = await Event.get(event.id)
            await event_to_delete.delete()
        return{"message":"all event successfully deleted"}
    except:
        response.status_code = 400
        return {"message":"something went wrong! or empty event list"}  
 
@router.delete("/delivery/{ID}", status_code = 200)
async def delete_a_delivery(ID:PydanticObjectId,response:Response) -> dict:
    try:
        delivery_to_delete = await Delivery.find_one(Delivery.id==ID, fetch_links=True)
        await delivery_to_delete.delete()
        return{"message":f"delivery with ID: {ID} successfully deleted"}
    except:
        response.status_code = 400
        return {"message":"something went wrong! or empty delivery list"}
    
    
       
@router.delete("/all/delivery", status_code = 200)
async def delete_all_delivery(response:Response) -> dict:
    try:
        deliverys = await Delivery.find_all().to_list()
        print(len(deliverys))
        for delivery in deliverys:
            delivery_to_delete = await Delivery.get(delivery.id)
            await delivery_to_delete.delete()
        return{"message":"all delivery successfully deleted"}
    except:
        response.status_code = 400
        return {"message":"something went wrong! or empty delivery list"}    
    
    
@router.delete("/user", status_code = 200)
async def delete_a_user(data:DeleteUser, response:Response) -> dict:
    try:
        user = await User.find_one(User.email == data.email)
        user_to_delete = await User.get(user.id)
        await user_to_delete.delete()
        return{"message":"user successfully deleted"}
    except:
        response.status_code = 400
        return {"message":"something went wrong! or user doesn't exist"}    
    