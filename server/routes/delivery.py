from fastapi import APIRouter, Depends,status,Response
from fastapi_jwt_auth import AuthJWT
from server.models.user import User
from ..utils import upload_image_helper
from ..settings import CONFIG_SETTINGS
from server.models.services import (Delivery,DeliveryImages,DeliverySchema)





router = APIRouter()


@router.post("/delivery",status_code=201)
async def create_delivery(data:DeliverySchema,response:Response, Authorize: AuthJWT = Depends()) -> dict:
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    
    user = await User.find_one(User.email == current_user)
    
    if CONFIG_SETTINGS.USE_SPACES:
        image_obj = await upload_image_helper.upload_image_to_S3_bucket(data.images,DeliveryImages)
    else:
        image_obj = await upload_image_helper.upload_image_to_file_path(data.images,DeliveryImages)
    try:            
        delivery = Delivery(
            title=data.title,
            pick_up_location=data.pick_up_location,
            delivery_location=data.delivery_location,
            category=data.category,
            delivery_type=data.delivery_type,
            size=data.size,
            select_category=data.select_category,
            price=data.price,
            description=data.description,
            image=image_obj,
            owner_id=user.id
            )
        
        await delivery.create()
        
        return {"message":"delivery successfully uploaded"}
    except:
        response.status_code = 400
        return {"message":"Something went wrong"}


