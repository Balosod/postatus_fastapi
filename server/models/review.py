from datetime import datetime

from beanie import Document, Link, PydanticObjectId
from pydantic import BaseModel
from typing import Optional

from .user import User


class ProductReview(Document):
    name: str
    product: str
    rating: float
    review: str
    date: datetime = datetime.now()
    author_id: Optional[PydanticObjectId]

    class Settings:
        name = "product_reviews"
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Jammie",
                "product": "Jammie Icecream",
                "rating": 4.9,
                "review": "Excellent!",
                "date": datetime.now()
            }
        }


class UpdateProductReview(BaseModel):
    name: Optional[str]
    product: Optional[str]
    rating: Optional[float]
    review: Optional[str]
    date: Optional[datetime]

    class Config:
        schema_extra = {
            "example": {
                "name": "Jammie",
                "product": "Jammie Icecream",
                "rating": 3.0,
                "review": "Excellent!",
                "date": datetime.now()
            }
        }