from fastapi import APIRouter, Depends,Query
from sqlmodel import Session
from db.session import get_db
import uuid
from typing import Optional,List
from schemas.user import Response
from schemas.products import ProductCreate,ProductUpdateData,ProductShow
from db.repository.product import create_product,all_products,update_product,get_product,delete_product

router = APIRouter()

@router.post("/create",response_model=Response)
def create_product_route(product:ProductCreate,db:Session=Depends(get_db)):
    return create_product(product=product,db=db)

@router.get("/all-products", response_model=List[ProductShow])
def show_all_products_route(min_price:Optional[float]=None,max_price:Optional[float]=None,certification_id:Optional[str]=Query(None),search:Optional[str]=None,db:Session=Depends(get_db),category_id: Optional[uuid.UUID] = None,subcategory_id: Optional[uuid.UUID] = None):
    return all_products(db=db,min_price=min_price,max_price=max_price, certification_id=certification_id,search=search, category_id=category_id, subcategory_id=subcategory_id)

@router.put("/update/{product_id}",response_model=Response)
def update_product_route(product_id:uuid.UUID,product:ProductUpdateData,db:Session=Depends(get_db)):
    return update_product(product_id=product_id,product=product,db=db)

@router.get("/{product_id}", response_model=None)
def get_product_by_id_route(product_id:uuid.UUID,db:Session=Depends(get_db)):
    return get_product(product_id=product_id,db=db)

@router.delete("/delete/{product_id}", response_model=None)
def delete_product_route(product_id:uuid.UUID,db:Session=Depends(get_db)):
    return delete_product(product_id=product_id,db=db)
