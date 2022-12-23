from typing import Optional,List
from beanie import Document, Link, PydanticObjectId
from pydantic import BaseModel







class Order(Document):
    owner_id: PydanticObjectId
    order_id: PydanticObjectId
    
    class Settings():
        name = "orders"
    