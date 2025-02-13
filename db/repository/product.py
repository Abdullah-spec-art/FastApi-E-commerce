from sqlmodel import Session,or_
from db.session import get_db
from fastapi import HTTPException, status, Depends,Query
from sqlmodel import select
from schemas.products import ProductCreate, ProductUpdateData, ProductShow
from db.repository.jwt import get_current_user
from db.models.product import Product
from schemas.user import Response
import uuid
from typing import Optional
from db.models.category import SubCategory
from db.models.certification import ProductCertification

def create_product(product:ProductCreate,db:Session):
    db_product=Product(name=product.name,description=product.description,price=product.price,stock=product.stock,category=product.category,image_url=product.image_url)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    data=ProductUpdateData(
        name=db_product.name,
        description=db_product.description,
        price=db_product.price,
        stock=db_product.stock,
        category=db_product.category,
        image_url=db_product.image_url
    )
    return Response[ProductUpdateData](data=data, message="The product added successfully")


def fetch_product_by_id(db:Session,product_id: uuid.UUID):
    stmt = select(Product).where(Product.id == product_id)
    result = db.exec(stmt).one_or_none()
    return result

def get_product(db:Session,product_id: uuid.UUID):
    stmt = select(Product).where(Product.id == product_id)
    db_product = db.exec(stmt).one_or_none()
    data=ProductShow(
        id=db_product.id,
        name=db_product.name,
        description=db_product.description,
        price=db_product.price,
        stock=db_product.stock,
        category=db_product.category,
        image_url=db_product.image_url
    )
    return Response[ProductShow](data=data, message="The product added successfully")

def update_product(product_id: uuid.UUID,product:ProductUpdateData, db:Session=Depends(get_db)):
    db_product=fetch_product_by_id(db,product_id)
    if not db_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="product not found.")
    if product.name is not None:
        db_product.name = product.name
    if product.description is not None:
        db_product.description = product.description
    if product.price is not None:
        db_product.price = product.price
    if product.stock is not None:
        db_product.stock = product.stock
    if product.category is not None:
        db_product.category = product.category
    if product.image_url is not None:
        db_product.image_url = product.image_url
    db.commit()
    db.refresh(db_product)
    data=ProductUpdateData(
        name=db_product.name,
        description=db_product.description,
        price=db_product.price,
        stock=db_product.stock,
        category=db_product.category,
        image_url=db_product.image_url
    )
    return Response[ProductUpdateData](data=data, message="The product updated successfully")
    

def delete_product(product_id: uuid.UUID,db:Session):
    db_product=fetch_product_by_id(db,product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="product not found") 
    db.delete(db_product)
    db.commit()
    return {"message":"product deleted successfully."}

def all_products(min_price:Optional[float]=None,max_price:Optional[float]=None,certification_id:Optional[str]=Query(None),search:Optional[str]=None,db:Session=Depends(get_db),category_id: Optional[uuid.UUID] = None,subcategory_id: Optional[uuid.UUID] = None):
    stmt = select(Product)
    if min_price is not None:
        stmt=stmt.where(Product.price>=min_price)
    if max_price is not None:
        stmt=stmt.where(Product.price<=max_price)
    if category_id:
         stmt = stmt.join(SubCategory).where(SubCategory.category_id == category_id)
    if subcategory_id:
        stmt = stmt.where(Product.category == subcategory_id)

    if certification_id:
        try:
            certification_uuid_list:list[uuid.UUID]=[
                uuid.UUID(cert.strip()) for cert in certification_id.split(",")
            ]
        except ValueError as e:
            raise HTTPException(status_code=400, detail="Invalid UUID format") from e
    else:
        certification_uuid_list = None

    if certification_uuid_list:
        stmt=stmt.join(ProductCertification).where(ProductCertification.certification_id.in_(certification_uuid_list)).distinct()
    if search:
        stmt = stmt.where(or_(Product.name.ilike(f"%{search}%"),Product.description.ilike(f"%{search}%")))

    


    products = db.exec(stmt).all()
    if not products:
        raise HTTPException(status_code=404, detail="Sorry, no product found")
    return [ProductShow(id=product.id,name=product.name,description=product.description,price=product.price,stock=product.stock,category=product.category,image_url=product.image_url) for product in products]

