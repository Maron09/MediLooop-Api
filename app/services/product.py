from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from decimal import Decimal

from app.models.product import Product
from app.models.inventory import Inventory
from app.errors.errors import ErrorMessages
from fastapi import HTTPException, status
from app.utils.modules import generate_sku



class ProductService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_product(
        self,
        *,
        pharmacy_id: UUID,
        name: str,
        sku: str,
        price: Decimal,
        initial_quantity: int,
    ) -> Product:
        result = await self.db.execute(
            select(Product)
            .where(
                Product.pharmacy_id == pharmacy_id,
                Product.name == name,
            )
        )
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=ErrorMessages.ERR_PRODUCT_ALREADY_EXISTS
            )
            
        sku_value = sku or generate_sku()
        
        product = Product(
            pharmacy_id=pharmacy_id,
            name=name,
            sku=sku_value,
            price=price,
        )
        
        self.db.add(product)
        await self.db.flush()
        
        inventory = Inventory(
            product_id=product.id,
            quantity=initial_quantity
        )
        
        self.db.add(inventory)
        
        return product