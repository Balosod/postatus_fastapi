from typing import Optional,List
from beanie import Document, Link, PydanticObjectId
from pydantic import BaseModel, EmailStr, Field,validator,HttpUrl
from enum import Enum
            
class Rating(int,Enum):
    zero = 0
    one = 1
    two = 2
    three = 3
    four = 4
    five = 5
    
class Feedback(Document):
    rating: Rating = Rating.zero
    review: Optional[str] = None
    item_id: PydanticObjectId
    
    class Settings():
        name = "feedback"
    
    
    
class FeedbackSchema(BaseModel):
    rating:Optional[Rating] = Rating.zero
    review: Optional[str] = None