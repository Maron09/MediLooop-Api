from uuid import UUID
from decimal import Decimal
from pydantic import BaseModel, Field




# ------------- INPUT SCHEMAS ------------- #

class ProductCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=255)
    price: Decimal = Field(..., gt=0)
    sku: str | None = Field(default=None, max_length=100)
    initial_quantity: int = Field(default=0, ge=0)



class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=255)
    price: Decimal | None = Field(default=None, gt=0)
    sku: str | None = Field(default=None, max_length=100)



# ------------- OUTPUT SCHEMAS ------------- #

class InventoryOut(BaseModel):
    quantity: int

    class Config:
        from_attributes = True


class ProductOut(BaseModel):
    id: UUID
    name: str
    price: Decimal
    sku: str | None
    inventory: InventoryOut

    class Config:
        from_attributes = True