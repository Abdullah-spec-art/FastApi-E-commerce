from pydantic import BaseModel, EmailStr
from typing import Optional,Generic, TypeVar
from datetime import datetime
import uuid

T = TypeVar("T")

class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock: int
    category: uuid.UUID
    image_url: Optional[str] = None


class ProductShow(BaseModel):
    id:uuid.UUID
    name: str
    description: Optional[str]
    price: float
    stock: int
    category: uuid.UUID
    image_url: Optional[str]

class ProductResponse(ProductCreate):
    id: int
    created_at: datetime
    updated_at: datetime

class ProductUpdateData(BaseModel):
    name: Optional[str]=None
    description: Optional[str]=None
    price: Optional[float]=None
    stock:Optional[int]=None
    category:Optional[uuid.UUID]=None
    image_url:Optional[str]=None

    class Config:
        arbitrary_types_allowed = True