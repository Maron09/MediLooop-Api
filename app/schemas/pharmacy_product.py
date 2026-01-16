from pydantic import BaseModel
from app.schemas.product import ProductOut
from typing import List




class ProductResponse(BaseModel):
    success: bool
    message: str
    product: ProductOut


class ProductsListResponse(BaseModel):
    success: bool
    message: str
    products: List[ProductOut]