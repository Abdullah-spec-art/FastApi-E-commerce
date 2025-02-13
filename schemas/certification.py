from pydantic import BaseModel, EmailStr
from typing import Optional,Generic, TypeVar,List
from datetime import datetime
import uuid
from db.models.certification import CertificationTypeEnum



class CertificationCreate(BaseModel):
    certification_type: CertificationTypeEnum 
    certification_name: str


class ProductCertificationCreate(BaseModel):
    product_id: uuid.UUID
    certification_id: list[uuid.UUID]

class ProductCertificationResponse(BaseModel):
    product_id: uuid.UUID
    certification_id: uuid.UUID