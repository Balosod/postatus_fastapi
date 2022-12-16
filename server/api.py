from fastapi import FastAPI, Request,Depends
from fastapi.responses import JSONResponse
from .db import init_db

from server.routes.users import router as UserRouter
from server.routes.services import router as ServicesRouter
from server.routes.explore_detail import router as exploreDetailRouter
from server.routes.explore import router as exploreRouter
from server.routes.interest import router as interestRouter


from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from .settings import CONFIG_SETTINGS
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/media", StaticFiles(directory="server/media"), name="media")
    

@AuthJWT.load_config
def get_config():
    return CONFIG_SETTINGS

@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )


app.include_router(UserRouter, tags=["Users"], prefix="/users")
app.include_router(ServicesRouter, tags=["services"], prefix="/services")
app.include_router(exploreRouter, tags=["explore"], prefix="/explore")
app.include_router(exploreDetailRouter, tags=["explore_detail"], prefix="/explore/detail")
app.include_router(interestRouter, tags=["interest"], prefix="/interest")



@app.on_event("startup")
async def start_db():
    await init_db()

@app.get("/", tags=["Root"])
async def read_root() -> dict:
    return {"message": "Welcome to postatus"}