from sqlmodel import Session
from db.session import get_db
from fastapi import HTTPException, status, Depends
from sqlmodel import select
from schemas.category import Create_category,ResponseData,ResponseCategory,CategoryWithSubCategories
from db.repository.jwt import get_current_user
from db.models.category import Category, SubCategory
from schemas.user import Response
import uuid
from typing import Optional
from sqlalchemy.orm import selectinload


def fetch_category(name: str,db: Session ):
    stmt = select(Category).where(Category.name==name)
    result = db.exec(stmt).one_or_none()
    return result

def get_category_by_id(category_id:uuid.UUID,db:Session):
    stmt = select(Category).where(Category.id==category_id)
    category = db.exec(stmt).one_or_none()
    data=ResponseCategory(
              id=category.id,
              name=category.name    
         )
    return Response[ResponseCategory](data=data,message="Category found successfully")
     
def create_category(user:Create_category, db:Session ):
    existing_category=fetch_category(user.name,db)
    if existing_category:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Category already exists"
            )
    db_category=Category(name=user.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    data=ResponseData(
         name=db_category.name
    )
    return Response[ResponseData](data=data, message="Category added sccessfully")

def get_categories(db:Session):
    stmt = select(Category)
    categories = db.exec(stmt).all()
    if categories is None:
        raise HTTPException(status_code=404, detail="category not found")
    return [ResponseCategory(id=category.id,name=category.name) for category in categories]


def get_categories_subcategories(db:Session):
    categories_stmt = select(Category)
    categories = db.exec(categories_stmt).all()
    data=[]
    if categories is None:
        raise HTTPException(status_code=404, detail="category not found")
    for category in categories:
        stmt = select(SubCategory).where(SubCategory.category_id==category.id)
        subcategories = db.exec(stmt).all()
        data.append(CategoryWithSubCategories(
            id=category.id,
            name=category.name,
            subcategories=[ResponseCategory(id=subcategory.id, name=subcategory.name)  for subcategory in subcategories]
        ))
    return data

def get_categories_subcategories_prac(db: Session):
    stmt = select(Category).options(selectinload(Category.subcategories))
    categories = db.exec(stmt).all()
    data=[CategoryWithSubCategories(
            id=category.id,
            name=category.name,
            subcategories=[ResponseCategory(id=subcategory.id, name=subcategory.name) for subcategory in category.subcategories]
         )
         for category in categories
    ]
    return data