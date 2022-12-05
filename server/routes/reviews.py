from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, Depends, Request
from typing import List


from server.models.review import ProductReview, UpdateProductReview
from server.models.user import User

# from auth.auth_bearer import JWTBearer
from fastapi_jwt_auth import AuthJWT


router = APIRouter()


@router.post("/", 
    response_description="Review added to the database", 
    # dependencies=[Depends(JWTBearer())]
)
async def add_product_review(review: ProductReview, Authorize: AuthJWT = Depends()) -> dict:
    # await review.create()
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()

    user = await User.find_one(User.email == current_user)
    review.author_id = user.id
    await review.save()

    return {"message": "Review successfully added!"}


@router.get("/", response_description="Review records retrieved")
async def get_all_reviews() -> List[ProductReview]:
    reviews = await ProductReview.find_all().to_list()
    return {"message": reviews}


@router.get("/{id}", response_description="Review record retrieved")
async def get_review(id: PydanticObjectId) -> ProductReview:
    review = await ProductReview.get(id)
    return {"message": review}


@router.put("/{id}", response_description="Update review item")
async def update_review(id: PydanticObjectId, data: UpdateProductReview) -> ProductReview:
    review = await ProductReview.get(id)
    if not review:
        raise HTTPException(
            status_code=404,
            detail="Review record not found!"
        )
    
    # validate the key has a value
    data = { k:v for k, v in data.dict().items() if v is not None }
    update_query = {"$set": {
        field: value for field, value in data.items()
    }}

    updated_review = await review.update(update_query)
    return {"message": review}


@router.delete("/{id}", response_description="Delete review item")
async def delete_review(id: PydanticObjectId) -> dict:
    review = await ProductReview.get(id)
    if not review:
        raise HTTPException(
            status_code=404,
            detail="Review record not found!"
        )

    await review.delete()
    return {"message": "Review has been deleted"}