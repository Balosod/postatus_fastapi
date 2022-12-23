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
        
        
        
         
class CommonBase(Document):
    category:CategoryChoices
    location:str
    price:int
    description:str
    tags:str
    average_ratings:Optional[int]=0
    total_reviews:Optional[int]=0
    owner_id: PydanticObjectId
    
    class Settings:
        is_root = True
        
    
class Product(CommonBase):
    what_to_sell: str
    quantity:int
    image: List[Link[ProductImages]]
    
    class Settings:
        name = "products"
        
       
class Service(CommonBase):
    what_to_do: str
    delivery_type:EventServicesDeliveryChoices
    duration:str
    image: List[Link[ServiceImages]]
    
    class Settings:
        name = "services"
        
        
class Event(CommonBase):
    what_is_it_about: str
    medium:EventServicesDeliveryChoices
    date_and_time:str
    image: List[Link[EventImages]]
    
    class Settings:
        name = "events"
        
        

class Delivery(Document):
    price:str
    description:str
    tags:str
    pick_up_location: str
    delivery_location:str
    category:DeliveryCategoryChoices
    delivery_type:DeliveryChoices
    size:str
    select_category:DeliveryChoices
    average_ratings:Optional[int]=0
    total_reviews:Optional[int]=0
    owner_id: PydanticObjectId
    
    class Settings:
        name = "deliverys"
        
        
class GoodsAndServiceEventSchema(BaseModel):
    #Common Schema
    category:Optional[CategoryChoices] = None
    location:Optional[str] = None
    price:Optional[int]=None
    description:Optional[str]=None
    tags:Optional[str]=None
    images:Optional[list] = None
    
    #Schema for Products
    what_to_sell: Optional[str] = None
    quantity:Optional[int] = None
    
    #Schema for Services
    what_to_do: Optional[str] = None
    delivery_type:Optional[EventServicesDeliveryChoices] = None
    duration:Optional[str] = None
    
    #Schema for Event
    what_is_it_about: Optional[str] = None
    medium:Optional[EventServicesDeliveryChoices] = None
    date_and_time:Optional[str] = None
    
    
class DeliverySchema(BaseModel):
    price:Optional[int]=None
    description:Optional[str]=None
    tags:Optional[str]=None
    pick_up_location: Optional[str] = None
    delivery_location:Optional[str] = None
    category:Optional[DeliveryCategoryChoices] = None
    delivery_type:Optional[DeliveryChoices] = None
    size: Optional[str] = None
    select_category:Optional[DeliveryChoices] = None
    
    
    