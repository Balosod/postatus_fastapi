from beanie import init_beanie
import motor.motor_asyncio

from server.models.user import User
from server.models.interest import Interest
from server.models.order_history import Order
from server.models.order_feedback import Feedback
from server.models.services import (
    CommonBase, Product,
    Service, Event, Delivery, 
    ProductImages, ServiceImages, 
    EventImages)

# from server.models.review import ProductReview


from .settings import CONFIG_SETTINGS

async def init_db():
    client = motor.motor_asyncio.AsyncIOMotorClient(CONFIG_SETTINGS.DATABASE_URL)
    db_name = client[CONFIG_SETTINGS.DATABASE_NAME]

    await init_beanie(database=db_name, document_models=[User,CommonBase,Product, Service,
                                                         Event, Delivery, ProductImages,
                                                         ServiceImages, EventImages,Interest,
                                                         Order,Feedback])

