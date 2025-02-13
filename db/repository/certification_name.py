from sqlmodel import Session
from db.session import get_db
from fastapi import HTTPException, status, Depends
from sqlmodel import select
from db.models.certification import ProductCertification
from schemas.certification import CertificationCreate,CertificationTypeEnum,ProductCertificationResponse,ProductCertificationCreate
import uuid
from typing import Optional


def add_product_certification(item:ProductCertificationCreate,db:Session):
    existing_certificates=db.exec(select(ProductCertification).where(ProductCertification.product_id==item.product_id,
                                                                     ProductCertification.certification_id.in_(item.certification_id))).all()
    if existing_certificates:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="One or more certifications already exist for this product"
        )
    db_entries=[ProductCertification(product_id=item.product_id,certification_id=cert_id) for cert_id in item.certification_id]
    db.add_all(db_entries)
    db.commit()
    for entry in db_entries:
        db.refresh(entry)
    return db_entries