from db.models.tablemodel import TableModel
from datetime import datetime, timezone
from sqlmodel import Field
import uuid
from typing import Optional

class Product(TableModel, table=True):
    __tablename__ = "Products"
    name: str = Field(nullable=False)
    description: str = Field(nullable=True)
    price: float = Field(nullable=False)
    stock: int = Field(nullable=False)
    category: uuid.UUID = Field(foreign_key="SubCategories.id",ondelete="CASCADE", nullable=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    image_url: str = Field(nullable=True)
    # created_by: uuid.UUID = Field(foreign_key="Users.id",ondelete="CASCADE", nullable=False)