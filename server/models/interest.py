from typing import Optional
from beanie import Document


class Interest(Document):
    interest:str
    
    class Settings:
        name:"interests"
