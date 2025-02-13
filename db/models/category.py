from db.models.tablemodel import TableModel
from sqlmodel import Field, Relationship
import uuid


class Category(TableModel, table=True):
    __tablename__ = "Categories"
    name: str = Field(nullable=False, unique=True)

    subcategories: list["SubCategory"] = Relationship(back_populates="category")




class SubCategory(TableModel, table=True):
    __tablename__ = "SubCategories"
    name: str = Field(nullable=False, unique=True)
    category_id: uuid.UUID = Field(foreign_key="Categories.id", ondelete="CASCADE", nullable=False)
    
    category: "Category" = Relationship(back_populates="subcategories")