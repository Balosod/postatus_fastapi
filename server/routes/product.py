from fastapi import APIRouter, Depends,status,Response
from fastapi_jwt_auth import AuthJWT
from server.models.user import User
from ..utils import upload_image_helper
from ..settings import CONFIG_SETTINGS
from server.models.services import (Product,ProductImages,ProductSchema)




router = APIRouter()

@router.post("/product",status_code=201)
async def create_product(data:ProductSchema,response:Response,Authorize: AuthJWT = Depends()) -> dict:
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    
    user = await User.find_one(User.email == current_user)
    try:
        if CONFIG_SETTINGS.USE_SPACES:
            image_obj = await upload_image_helper.upload_image_to_S3_bucket(data.images,ProductImages)
        else:
            image_obj = await upload_image_helper.upload_image_to_file_path(data.images,ProductImages)
        
        product = Product(
            title=data.title,
            quantity=data.quantity,
            category=data.category,
            location=data.location,
            price=data.price,
            description=data.description,
            image=image_obj,
            owner_id=user.id
            )
        
        await product.create()
        
        return {"message":"product successfully uploaded"}
    except:
        response.status_code = 400
        return {"message":"Something went wrong"}
    