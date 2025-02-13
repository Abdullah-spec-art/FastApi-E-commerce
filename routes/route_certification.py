from fastapi import APIRouter, Depends,Query
from sqlmodel import Session
from db.session import get_db
from typing import Optional,List
from schemas.certification import CertificationCreate, CertificationTypeEnum,ProductCertificationCreate
from db.repository.certification import create_certification, get_all_certification_type_names,get_all_certification_names
from schemas.user import Response
from db.repository.certification_name import add_product_certification
import uuid

router = APIRouter()

@router.post("/create-product-certification", response_model=None) 
def create_product_certification_route(item:ProductCertificationCreate,db:Session=Depends(get_db)):
    return add_product_certification(item=item,db=db)

@router.post("/create", response_model=None)
def create_certification_route(certification_data:CertificationCreate,db:Session=Depends(get_db)):
    return create_certification(certification_data=certification_data,db=db)


@router.get("/all-certifications",response_model=None)
def all_certification_types_names_route(certification_type:Optional[list[CertificationTypeEnum]]=Query(None),search:Optional[str]=None,db:Session=Depends(get_db)):
    return get_all_certification_type_names(db=db, certification_type=certification_type, search=search)

@router.get("/certification-names",response_model=None)
def all_certification_names_by_type_route(general_search:Optional[str] = None,subcategory_id:Optional[uuid.UUID]=None,category_id:Optional[uuid.UUID]=None,db:Session=Depends(get_db)):
    return get_all_certification_names(general_search=general_search,subcategory_id=subcategory_id,category_id=category_id, db=db)


