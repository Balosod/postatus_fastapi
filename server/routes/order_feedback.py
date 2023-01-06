from fastapi import APIRouter, Depends, Response, status
from fastapi_jwt_auth import AuthJWT
from beanie import PydanticObjectId
from beanie.operators import And
from server.models.order_history import Order
from server.models.order_feedback import Feedback, FeedbackSchema
from server.models.user import User
from server.models.services import (Product, Service, Event,Delivery)



router = APIRouter()


async def get_ID(itemID):
    product = await Product.get(itemID, fetch_links=True)
    if product:
        return product.id
    service = await Service.get(itemID, fetch_links=True)
    if service:
        return service.id
    event = await Event.get(itemID, fetch_links=True)
    if event:
        return event.id
    delivery = await Delivery.get(itemID, fetch_links=True)
    if delivery:
        return delivery.id
    else:
        return None
    
async def update_rate(itemID,ratings_average):
    product = await Product.get(itemID, fetch_links=True)
    if product:
        product.average_ratings = ratings_average
        await product.save()
        return
    service = await Service.get(itemID, fetch_links=True)
    if service:
        service.average_ratings = ratings_average
        await service.save()
        return
    event = await Event.get(itemID, fetch_links=True)
    if event:
        event.average_ratings = ratings_average
        await event.save()
        return
    delivery = await Delivery.get(itemID, fetch_links=True)
    if delivery:
        delivery.average_ratings = ratings_average
        await delivery.save()
        return
    else:
        return None
    
async def update_rivew(itemID,reviews_total):
    product = await Product.get(itemID, fetch_links=True)
    if product:
        product.total_reviews = reviews_total
        await product.save()
        return
    service = await Service.get(itemID, fetch_links=True)
    if service:
        service.total_reviews = reviews_total
        await service.save()
        return
    event = await Event.get(itemID, fetch_links=True)
    if event:
        event.total_reviews = reviews_total
        await event.save()
        return
    delivery = await Delivery.get(itemID, fetch_links=True)
    if delivery:
        delivery.total_reviews = reviews_total
        await delivery.save()
        return
    else:
        return None
    
@router.post("/{itemID}",status_code = 201)
async def create_ratings_and_reviews(data :FeedbackSchema,itemID:PydanticObjectId,response:Response, Authorize: AuthJWT = Depends()) -> dict:
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    
    user = await User.find_one(User.email == current_user)
    Id = await get_ID(itemID)

    if Id:
        order_exist = await Order.find_one(And((Order.order_id == Id), (Order.owner_id == user.id)))
        if order_exist:
            feedback = Feedback(
                rating=data.rating,
                review=data.review,
                item_id=Id
            )
            await feedback.create()
            
            # Calculate average ratings for Product, Services and Event
            rate_count = 0
            ratings_obj = await Feedback.find(And((Feedback.rating >= 1),(Feedback.item_id == Id))).to_list()
            for rate in ratings_obj:
                rate_count+=rate.rating.value
            divisor = len(ratings_obj)
            ratings_average = round((rate_count/divisor),1)
            await update_rate(itemID,ratings_average)
            
            # Calculate total revies for Product, Services and Event
            reviews_obj = await Feedback.find(And((And((Feedback.review != None),(Feedback.review != ''))),(Feedback.item_id == Id))).to_list()
            reviews_total = len(reviews_obj)
            await update_rivew(itemID,reviews_total)
           
            return {"message":"Feedback created"}
        else:
            response.status_code = 400
            return {"message":"You haven't order this product/services/event"}
    else:
        response.status_code = 400
        return {"message":"Product/Service/Event doesn't exit any more"}