from fastapi import APIRouter, Depends
from sqlmodel import Session
from db.session import get_db
from typing import Optional,List
from schemas.category import ResponseData,Create_category,ResponseCategory
from db.repository.category import create_category,get_categories,get_category_by_id,get_categories_subcategories,get_categories_subcategories_prac
from schemas.user import Response
import uuid

router = APIRouter()


@router.post("/create", response_model=Response)
def create_category_route(user:Create_category,db:Session=Depends(get_db)):
    return create_category(user=user, db=db)

@router.get("/all-categories", response_model=list[ResponseCategory])
def get_categories_route(db:Session=Depends(get_db)):
    return get_categories(db=db)

@router.get("/all-categories-subcategories", response_model=None)
def get_categories_subcategories_route(db:Session=Depends(get_db)):
    return get_categories_subcategories(db=db)

@router.get("/all-categories-subcategories-prac", response_model=None)
def get_categories_subcategories_prac_route(db:Session=Depends(get_db)):
    return get_categories_subcategories_prac(db=db)
 
@router.get("/{category_id}", response_model=Response)
def get_category_route(category_id:uuid.UUID, db:Session=Depends(get_db)):
    return get_category_by_id(category_id=category_id,db=db)


