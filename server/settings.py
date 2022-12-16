from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from decouple import config
from pydantic import BaseModel
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig,MessageType



class Settings(BaseModel):
    authjwt_secret_key = config("SECRET")
    authjwt_access_token_expires = 86400
    authjwt_algorithm = "HS256"
    DATABASE_URL = config("DATABASE_URL")
    DATABASE_NAME = config("DATABASE_NAME")
    ALGORITHM = config("ALGORITHM")
    
    MAIL_USERNAME = config("MAIL_USERNAME")
    MAIL_PASSWORD = config("MAIL_PASSWORD")
    MAIL_FROM = config("MAIL_FROM")
    MAIL_SERVER = config("MAIL_SERVER")
    
    OTP_SECRET_KEY=config("OTP_SECRET_KEY")
    OTP_EXPIRES=config("OTP_EXPIRES")
    
    
conf = ConnectionConfig(
    MAIL_USERNAME = config("MAIL_USERNAME"),
    MAIL_PASSWORD = config("MAIL_PASSWORD"),
    MAIL_FROM = config("MAIL_FROM"),
    MAIL_PORT = 465,
    MAIL_SERVER = config("MAIL_SERVER"),
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS = True,
)
 
CONFIG_SETTINGS = Settings()