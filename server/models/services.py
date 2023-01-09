from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional,List
from beanie import Document, Link, PydanticObjectId
from pydantic import BaseModel, EmailStr, Field,validator,HttpUrl
from enum import Enum


     
        
class CategoryChoices(str,Enum):
    FOOD_AND_DRINKS = "FOOD_AND_DRINKS"
    GRAPHIC_DESIGN = "GRAPHIC_DESIGN"
    RECREATIONAL_AND_FUN_FAIR = 'RECREATIONAL_AND_FUN_FAIR'
    
    
class EventServicesDeliveryChoices(str,Enum):
    ONLINE = "ONLINE"
    OFFLINE = "OFFLINE"


class DeliveryCategoryChoices(str,Enum):
    INTER_STATE = "INTER_STATE"
    WITHIN_STATE = "WITHIN_STATE"
    
    
class DeliveryChoices(str,Enum):
    MOTOR_CYCLE = "MOTOR_CYCLE"
    MINI_VAN = "MINI_VAN"
    TRUCK = "TRUCK"
    



class ProductImages(Document):
    img:str
    
    class Settings:
        name = "products_image"
        
class ServiceImages(Document):
    img:str
    
    class Settings:
        name = "services_image"
        
class EventImages(Document):
    img:str
    
    class Settings:
        name = "events_image"
        
class DeliveryImages(Document):
    img:str
    
    class Settings:
        name = "deliverys_image"
        
        
        
         
class CommonBase(Document):
    category:CategoryChoices
    location:str
    price:int
    description:str
    liked:bool = False
    average_ratings:Optional[int]=0
    total_reviews:Optional[int]=0
    owner_id: PydanticObjectId
    
    class Settings:
        is_root = True
        
    
class Product(CommonBase):
    title: str
    quantity:int
    types:str = "product"
    image: List[Link[ProductImages]]
    
    class Settings:
        name = "products"
        
       
class Service(CommonBase):
    title: str
    delivery_type:EventServicesDeliveryChoices
    duration:str
    types:str = "service"
    image: List[Link[ServiceImages]]
    
    class Settings:
        name = "services"
        
        
class Event(CommonBase):
    title: str
    medium:EventServicesDeliveryChoices
    date_and_time:str
    types:str = "event"
    image: List[Link[EventImages]]
    
    class Settings:
        name = "events"
        
        

class Delivery(Document):
    title: str
    price:str
    description:str
    liked:bool = False
    types:str = "delivery"
    pick_up_location: str
    delivery_location:str
    category:DeliveryCategoryChoices
    delivery_type:DeliveryChoices
    size:str
    select_category:DeliveryChoices
    average_ratings:Optional[int]=0
    total_reviews:Optional[int]=0
    owner_id: PydanticObjectId
    image: List[Link[DeliveryImages]]
    
    class Settings:
        name = "deliverys"
        

    
class ProductSchema(BaseModel):
    title: str
    quantity:int
    category:CategoryChoices
    location:str
    price:int
    description:str
    images:list
    
class ServiceSchema(BaseModel):
    title: str
    delivery_type:EventServicesDeliveryChoices
    duration:str
    category:CategoryChoices
    location:str
    price:int
    description:str
    images:list
    
class EventSchema(BaseModel):
    title: str
    medium:EventServicesDeliveryChoices
    date_and_time:str
    category:CategoryChoices
    location:str
    price:int
    description:str
    images:list
    
   
class DeliverySchema(BaseModel):
    title: str
    price:Optional[int]=None
    description:Optional[str]=None
    pick_up_location: Optional[str] = None
    delivery_location:Optional[str] = None
    category:Optional[DeliveryCategoryChoices] = None
    delivery_type:Optional[DeliveryChoices] = None
    size: Optional[str] = None
    select_category:Optional[DeliveryChoices] = None
    images:Optional[list] = None
    
    
    
    
class ExploreSearch(BaseModel):
    search:str
    
    
    