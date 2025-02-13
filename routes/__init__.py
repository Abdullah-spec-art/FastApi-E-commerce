from fastapi import APIRouter

from routes import route_user
from routes import route_product
from routes import route_category
from routes import route_subcategory
from routes import route_certification


router=APIRouter()

router.include_router(route_user.router, prefix="/user",tags=["User"])
router.include_router(route_product.router, prefix="/product",tags=["Product"])
router.include_router(route_category.router, prefix="/product/category",tags=["Category"])
router.include_router(route_subcategory.router, prefix="/product/subcategory",tags=["SubCategory"])
router.include_router(route_certification.router, prefix="/product/certification",tags=["Certification"])

__all__ = ["router"]