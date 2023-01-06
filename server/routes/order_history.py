from fastapi import APIRouter, Depends, Response, status
from fastapi_jwt_auth import AuthJWT
from beanie import PydanticObjectId
from server.models.order_history import Order
from server.models.user import User
from server.models.services import (Product, Service, Event,Delivery)



router = APIRouter()


async def get_ID(itemID):
    product = await Product.get(itemID, fetch_links=True)
    if product:
        print("for product")
        return product.id
    service = await Service.get(itemID, fetch_links=True)
    if service:
        print("for service")
        return service.id
    event = await Event.get(itemID, fetch_links=True)
    if event:
        print("for event")
        return event.id
    else:
        return None
    

@router.get("/{itemID}", status_code = 200)
async def create_order(itemID:PydanticObjectId,response:Response, Authorize: AuthJWT = Depends()) -> dict:
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    
    user = await User.find_one(User.email == current_user)
    Id = await get_ID(itemID)

    if Id:
        order = Order(
            owner_id=user.id,
            order_id=Id
            )
        
        await order.create()
        previous_user_order = user.my_order
        user.my_order = previous_user_order + 1
        await user.save()
        return {"message":"Order successfully added"}
    else:
        response.status_code = 400
        return HTTPException(
            status_code=400,
            detail="Product/Service/Event doesn't exit any more"
        )
    
    
