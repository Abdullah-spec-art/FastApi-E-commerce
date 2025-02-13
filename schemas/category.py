from pydantic import BaseModel, EmailStr
from typing import Optional,Generic, TypeVar,List
from datetime import datetime
import uuid

T = TypeVar("T")

class Create_category(BaseModel):
    name: str

class ResponseData(BaseModel):
    name: str

class ResponseCategory(BaseModel):
    id:uuid.UUID
    name: str

class CategoryWithSubCategories(BaseModel):
    id: uuid.UUID
    name: str
    subcategories: List[ResponseCategory] 
    
    class Config:
        arbitrary_types_allowed = True