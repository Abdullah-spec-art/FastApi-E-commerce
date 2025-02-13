from db.models.tablemodel import TableModel
from sqlmodel import Field
import uuid
from typing import Optional
from enum import Enum

class CertificationTypeEnum(str, Enum):
    PRODUCT = "Product"
    SUPPLIER = "Supplier"

    @classmethod
    def _missing_(cls, value):
        for member in cls:
            if member.value.lower() == value.lower():
                return member
        return None 

class Certification(TableModel, table=True):
    __tablename__ = "Certifications"
    certification_type: CertificationTypeEnum = Field(nullable=False)
    certification_name: Optional[str] = Field(nullable=True) 


class ProductCertification(TableModel, table=True):
    __tablename__ = "ProductCertifications"
    product_id: uuid.UUID = Field(foreign_key="Products.id", primary_key=True)
    certification_id: uuid.UUID = Field(foreign_key="Certifications.id", primary_key=True)
    