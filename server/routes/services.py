from fastapi import APIRouter, Depends,status,Response
from fastapi_jwt_auth import AuthJWT
from server.models.user import User
import base64
import uuid
from ..utils.s3_storage import client
from ..settings import CONFIG_SETTINGS
from server.models.services import (Product, Service, Event, 
                                    Delivery, ProductImages,
                                    ServiceImages, EventImages,DeliveryImages,
                                    GoodsAndServiceEventSchema,DeliverySchema)




router = APIRouter()

async def upload_image_to_file_path(images,model_name):
    image_obj_list = []
    for image in images:
        img_name = str(uuid.uuid4())[:10] + '.png'
        image_as_bytes = str.encode(image) 
        img_recovered = base64.b64decode(image_as_bytes)
        
        with open("server/media/image/uploaded_" + img_name, "wb") as f:
            f.write(img_recovered)
            
        upload_image = model_name(img=f"http://localhost:8000/media/image/uploaded_{img_name}")
        image_obj_list.append(upload_image)
        await upload_image.create()
    return image_obj_list
    
async def upload_image_to_S3_bucket(images,model_name):
    image_obj_list = []
    for image in images:
        img_name = str(uuid.uuid4())[:10] + '.png'
        image_as_bytes = str.encode(image) 
        img_recovered = base64.b64decode(image_as_bytes)
        
        client.put_object(
        Bucket=CONFIG_SETTINGS.BUCKET,
        Body=img_recovered,
        Key=f"image/{img_name}",
        ACL=CONFIG_SETTINGS.ACL,
        ContentType="image/png"
        )
            
        upload_image = model_name(img=f"https://postatusapistorage.nyc3.digitaloceanspaces.com/image/{img_name}")
        image_obj_list.append(upload_image)
        await upload_image.create()
    return image_obj_list

@router.post("/services",status_code=201)
async def create_services(data:GoodsAndServiceEventSchema,response:Response,Authorize: AuthJWT = Depends()) -> dict:
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    
    user = await User.find_one(User.email == current_user)
    try:
        if data.what_to_sell:
            if CONFIG_SETTINGS.USE_SPACES:
                image_obj = await upload_image_to_S3_bucket(data.images,ProductImages)
            else:
                image_obj = await upload_image_to_file_path(data.images,ProductImages)
            
            product = Product(
                what_to_sell=data.what_to_sell,
                quantity=data.quantity,
                category=data.category,
                location=data.location,
                price=data.price,
                description=data.description,
                # tags=data.tags,
                image=image_obj,
                owner_id=user.id
                )
            
            await product.create()
            
            return {"message":"product successfully uploaded"}
    except:
        pass
    
    try:
        if data.what_to_do:
            
            if CONFIG_SETTINGS.USE_SPACES:
                image_obj = await upload_image_to_S3_bucket(data.images,ServiceImages)
            else:
                image_obj = await upload_image_to_file_path(data.images,ServiceImages)
            
            service = Service(
                what_to_do=data.what_to_do,
                delivery_type=data.delivery_type,
                duration=data.duration,
                category=data.category,
                location=data.location,
                price=data.price,
                description=data.description,
                # tags=data.tags,
                image=image_obj,
                owner_id=user.id
                )
            
            await service.create()
            
            return {"message":"service successfully uploaded"}
    except:
        pass
    
    try:
        if data.what_is_it_about:
            
            if CONFIG_SETTINGS.USE_SPACES:
                image_obj = await upload_image_to_S3_bucket(data.images,EventImages)
            else:
                image_obj = await upload_image_to_file_path(data.images,EventImages)
            
            event = Event(
                what_is_it_about=data.what_is_it_about,
                medium=data.medium,
                date_and_time=data.date_and_time,
                category=data.category,
                location=data.location,
                price=data.price,
                description=data.description,
                # tags=data.tags,
                image=image_obj,
                owner_id=user.id
                )
            
            await event.create()
            
            return {"message":"event successfully uploaded"}
    except:
        pass
    response.status_code = 400
    return {"message":"Something went wrong"}




@router.post("/delivery",status_code=201)
async def create_delivery(data:DeliverySchema,response:Response, Authorize: AuthJWT = Depends()) -> dict:
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    
    user = await User.find_one(User.email == current_user)
    
    if CONFIG_SETTINGS.USE_SPACES:
        image_obj = await upload_image_to_S3_bucket(data.images,DeliveryImages)
    else:
        image_obj = await upload_image_to_file_path(data.images,DeliveryImages)
    try:            
        delivery = Delivery(
            pick_up_location=data.pick_up_location,
            delivery_location=data.delivery_location,
            category=data.category,
            delivery_type=data.delivery_type,
            size=data.size,
            select_category=data.select_category,
            price=data.price,
            description=data.description,
            # tags=data.tags,
            image=image_obj,
            owner_id=user.id
            )
        
        await delivery.create()
        
        return {"message":"delivery successfully uploaded"}
    except:
        response.status_code = 400
        return {"message":"Something went wrong"}
