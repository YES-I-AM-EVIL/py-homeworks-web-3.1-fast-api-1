from pydantic import BaseModel
from datetime import datetime

class AdvertisementBase(BaseModel):
    title: str
    description: str
    price: float
    author: str

class AdvertisementCreate(AdvertisementBase):
    pass

class AdvertisementResponse(AdvertisementBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True