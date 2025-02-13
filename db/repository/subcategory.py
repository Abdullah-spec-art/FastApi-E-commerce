from sqlmodel import Session
from db.session import get_db
from fastapi import HTTPException, status, Depends
from sqlmodel import select
from schemas.category import Create_category,ResponseData,ResponseCategory
from db.repository.jwt import get_current_user
from db.models.category import Category, SubCategory
from schemas.user import Response
import uuid

def fetch_category_id(db: Session, category_id:uuid.UUID):
    stmt = select(Category).where(Category.id==category_id)
    result = db.exec(stmt).one_or_none()
    return result

def get_subcategory_by_id(category_id:uuid.UUID,db:Session):
    stmt = select(Category).where(Category.id==category_id)
    category = db.exec(stmt).one_or_none()
    data=ResponseCategory(
              id=category.id,
              name=category.name    
         )
    return Response[ResponseCategory](data=data,message="Category found successfully")

def create_subcategories(db:Session, category:Create_category, category_id:uuid.UUID):
    main_category=fetch_category_id(db,category_id)
    if main_category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    stmt = select(SubCategory).where(SubCategory.name==category.name)
    existing_subcategory=db.exec(stmt).one_or_none()
    if existing_subcategory:
        raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Category already exists"
            )

    db_category=SubCategory(name=category.name, category_id=category_id)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    data=ResponseData(
         name=db_category.name
    )
    return Response[ResponseData](data=data, message="SubCategory added sccessfully")



def get_subcategories(db:Session,category_id:uuid.UUID):
    stmt = select(SubCategory).where(SubCategory.category_id==category_id)
    categories = db.exec(stmt).all()
    if categories is None:
        raise HTTPException(status_code=404, detail="category not found")
    return [ResponseCategory(id=category.id,name=category.name) for category in categories]

