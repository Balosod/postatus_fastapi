from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT
from server.models.user import User
import base64
import uuid
from server.models.services import (Product, Service, Event, 
                                    Delivery, ProductImages,
                                    ServiceImages, EventImages, 
                                    GoodsAndServiceEventSchema,DeliverySchema)



router = APIRouter()

@router.post("/")
async def create_services(data:GoodsAndServiceEventSchema,Authorize: AuthJWT = Depends()) -> dict:
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    
    user = await User.find_one(User.email == current_user)
    image_obj = []
    try:
        if data.what_to_sell:
            for image in data.images:
                img_name = str(uuid.uuid4())[:10] + '.png'
                image_as_bytes = str.encode(image) 
                img_recovered = base64.b64decode(image_as_bytes)
                
                with open("server/media/image/uploaded_" + img_name, "wb") as f:
                    f.write(img_recovered)
                    
                upload_image = ProductImages(img=f"http://localhost:8000/media/image/uploaded_{img_name}")
                image_obj.append(upload_image)
                await upload_image.create()
            
            product = Product(
                what_to_sell=data.what_to_sell,
                quantity=data.quantity,
                category=data.category,
                location=data.location,
                price=data.price,
                description=data.description,
                tags=data.tags,
                image=image_obj,
                owner_id=user.id
                )
            
            await product.create()
            
            return {"message":"product successfully uploaded"}
    except:
        pass
    
    try:
        if data.what_to_do:
            for image in data.images:
                img_name = str(uuid.uuid4())[:10] + '.png'
                image_as_bytes = str.encode(image) 
                img_recovered = base64.b64decode(image_as_bytes)
                
                with open("server/media/image/uploaded_" + img_name, "wb") as f:
                    f.write(img_recovered)
                    
                upload_image = ServiceImages(img=f"http://localhost:8000/media/image/uploaded_{img_name}")
                image_obj.append(upload_image)
                await upload_image.create()
            
            service = Service(
                what_to_do=data.what_to_do,
                delivery_type=data.delivery_type,
                duration=data.duration,
                category=data.category,
                location=data.location,
                price=data.price,
                description=data.description,
                tags=data.tags,
                image=image_obj,
                owner_id=user.id
                )
            
            await service.create()
            
            return {"message":"service successfully uploaded"}
    except:
        pass
    
    try:
        if data.what_is_it_about:
            for image in data.images:
                img_name = str(uuid.uuid4())[:10] + '.png'
                image_as_bytes = str.encode(image) 
                img_recovered = base64.b64decode(image_as_bytes)
                
                with open("server/media/image/uploaded_" + img_name, "wb") as f:
                    f.write(img_recovered)
                    
                upload_image = EventImages(img=f"http://localhost:8000/media/image/uploaded_{img_name}")
                image_obj.append(upload_image)
                await upload_image.create()
            
            event = Event(
                what_is_it_about=data.what_is_it_about,
                medium=data.medium,
                date_and_time=data.date_and_time,
                category=data.category,
                location=data.location,
                price=data.price,
                description=data.description,
                tags=data.tags,
                image=image_obj,
                owner_id=user.id
                )
            
            await event.create()
            
            return {"message":"event successfully uploaded"}
    except:
        pass
    
    return {"message":"Something went wrong"}




@router.post("/delivery")
async def create_delivery(data:DeliverySchema,Authorize: AuthJWT = Depends()) -> dict:
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    
    user = await User.find_one(User.email == current_user)
    delivery = Delivery(
        pick_up_location=data.pick_up_location,
        delivery_location=data.delivery_location,
        category=data.category,
        delivery_type=data.delivery_type,
        size=data.size,
        select_category=data.select_category,
        price=data.price,
        description=data.description,
        tags=data.tags,
        owner_id=user.id
        )
    
    await delivery.create()
    
    return {"message":"delivery successfully uploaded"}



@router.get("/findall", response_description="all data")
async def create_account() -> dict:
    
    data1 = await Product.find(
    Product.what_to_sell == "phone", 
    fetch_links=True
    ).to_list()
    data2 = await Service.find(
    Service.what_to_do == "Build website", 
    fetch_links=True
    ).to_list()
    data3 = await Event.find(
    Event.what_is_it_about == "Wedding", 
    fetch_links=True
    ).to_list()
    data4 = await Delivery.find(
    Delivery.pick_up_location == "Osogbo", 
    fetch_links=True
    ).to_list()
    
    

    
    return {"product":data1,"service":data2,"event":data3,"delivery":data4}
