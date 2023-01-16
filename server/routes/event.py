from fastapi import APIRouter, Depends,status,Response
from fastapi_jwt_auth import AuthJWT
from server.models.user import User
from ..utils import upload_image_helper
from ..settings import CONFIG_SETTINGS
from ..utils.location_manager import get_location
from server.models.services import ( Event, EventImages,EventSchema)




router = APIRouter()

@router.post("/event/{latitude}/{longitude}",status_code=201)
async def create_event(data:EventSchema, latitude:float,longitude:float,response:Response,Authorize: AuthJWT = Depends()) -> dict:
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    
    user = await User.find_one(User.email == current_user)
    
    get_address = get_location(latitude,longitude)
    
    if get_address:
        try:
            location = f"{get_address['city']} {get_address['state']},{get_address['country']}"
        except:
           location = f"{get_address['state']},{get_address['country']}"
           
    else:
        location = ""
        
    try:
       
        if CONFIG_SETTINGS.USE_SPACES:
            image_obj = await upload_image_helper.upload_image_to_S3_bucket(data.images,EventImages)
        else:
            image_obj = await upload_image_helper.upload_image_to_file_path(data.images,EventImages)
        
        event = Event(
            title=data.title,
            medium=data.medium,
            date_and_time=data.date_and_time,
            category=data.category,
            location=location,
            price=data.price,
            description=data.description,
            image=image_obj,
            owner_id=user.id
            )
        
        await event.create()
        
        return {"message":"event successfully uploaded"}
    except:
        response.status_code = 400
        return {"message":"Something went wrong"}
    