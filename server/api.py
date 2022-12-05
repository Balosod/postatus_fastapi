from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from .db import init_db
from server.routes.reviews import router as ReviewRouter
from server.routes.users import router as UserRouter


from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel
from fastapi_jwt_auth.exceptions import AuthJWTException



app = FastAPI()


class Settings(BaseModel):
    authjwt_secret_key: str = "secret"

    

@AuthJWT.load_config
def get_config():
    return Settings()

@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )


app.include_router(ReviewRouter, tags=["Reviews"], prefix="/reviews")
app.include_router(UserRouter, tags=["Users"], prefix="/users")


@app.on_event("startup")
async def start_db():
    await init_db()

@app.get("/", tags=["Root"])
async def read_root() -> dict:
    return {"message": "Welcome to your beanie powered app!"}