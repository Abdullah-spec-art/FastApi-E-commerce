from fastapi import APIRouter, Depends
from sqlmodel import Session
from db.session import get_db
import uuid
from typing import Optional,List
from schemas.category import ResponseData,Create_category,ResponseCategory
from db.repository.subcategory import create_subcategories,get_subcategories
from schemas.user import Response
import uuid

router = APIRouter()


@router.post("/create/{category_id}", response_model=Response)
def create_subcategory_route( category_id:uuid.UUID,category:Create_category,db:Session=Depends(get_db)):
    return create_subcategories(category_id=category_id,category=category, db=db )



@router.get("/{category_id}", response_model=list[ResponseCategory])
def get_subcategories_route(category_id:uuid.UUID,db:Session=Depends(get_db)):
    return get_subcategories(category_id=category_id,db=db )
