from sqlmodel import Session
from db.session import get_db
from fastapi import HTTPException, status, Depends
from sqlmodel import select, func,or_,and_
from db.models.certification import Certification
from schemas.certification import CertificationCreate,CertificationTypeEnum
import uuid
from typing import Optional
from db.models.certification import ProductCertification
from db.models.product import Product
from db.models.category import Category,SubCategory



def create_certification(certification_data:CertificationCreate,db:Session):
    stmt=select(Certification).where(Certification.certification_name==certification_data.certification_name)
    existing_certification=db.exec(stmt).one_or_none()
    if existing_certification:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Certification name already exist"
        )
    db_certification=Certification(certification_type=certification_data.certification_type,certification_name=certification_data.certification_name)
    db.add(db_certification)
    db.commit()
    db.refresh(db_certification)
    data=CertificationCreate(
        certification_type=db_certification.certification_type,
        certification_name=db_certification.certification_name
    )

    return data


def get_all_certification_type_names(db:Session,product_search:Optional[str]=None,supplier_search:Optional[str]=None,certification_type:Optional[list[CertificationTypeEnum]]=None):
    if certification_type:
        stmt = select(Certification).where(Certification.certification_type.in_(certification_type))
    
    if product_search:
        stmt = stmt.where(Certification.certification_type == "Product",Certification.certification_name.ilike(f"%{product_search}%"))
    if supplier_search:
        stmt = stmt.where(Certification.certification_type == "Supplier",Certification.certification_name.ilike(f"%{supplier_search}%"))
    result = db.exec(stmt).all()
    return [
        {"id": row.id, "certification_name": row.certification_name, "certification_type":certification_type}
        for row in result
    ]

    

def get_all_certification_names(db:Session,general_search:Optional[str]=None,subcategory_id:Optional[uuid.UUID]=None,category_id:Optional[uuid.UUID]=None):
    stmt = (
        select(
            Certification.certification_type,
            func.json_agg(
                func.json_build_object(
                    'id', Certification.id, 
                    'certification_name', Certification.certification_name
                )
            )
        ).group_by(Certification.certification_type).order_by(Certification.certification_type)
    )
    
    if category_id or subcategory_id or general_search:
        stmt = stmt.join(ProductCertification, ProductCertification.certification_id == Certification.id) \
                   .join(Product, Product.id == ProductCertification.product_id)

    if category_id:
        stmt=stmt.join(SubCategory, SubCategory.id == Product.category)\
            .join(Category,Category.id==SubCategory.category_id)\
            .where(Category.id == category_id)
    
    if subcategory_id:
        stmt=stmt.join(SubCategory, SubCategory.id == Product.category).where(SubCategory.id == subcategory_id)
        
    if general_search:
        stmt=stmt.where(Product.name.ilike(f"%{general_search}%"))

        
    stmt = stmt

    result = db.exec(stmt).fetchall()

    return [{"certification_type": row.certification_type, "certifications": row.json_agg} for row in result]









# stmt = stmt.group_by(Certification.certification_type).order_by(Certification.certification_type)