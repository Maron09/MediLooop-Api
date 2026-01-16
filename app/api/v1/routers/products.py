from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.sessions import get_db
from app.core.context import PharmacyContext
from app.api.permissions import require_owner_or_staff
from app.services.product import ProductService
from app.api.deps import get_product_service
from app.schemas.product import ProductCreate
from app.schemas.pharmacy_product import ProductResponse, ProductsListResponse, ProductOut
from app.errors.errors import ErrorMessages
from app.messages.messages import Messages

router = APIRouter(prefix="/pharmacies", tags=["Products"])

@router.post(
    "/{pharmacy_id}/products",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_product_endpoint(
    payload: ProductCreate,
    db: AsyncSession = Depends(get_db),
    ctx: PharmacyContext = Depends(require_owner_or_staff),
):
    product_service = ProductService(db)

    try:
        product = await product_service.create_product(
            pharmacy_id=ctx.pharmacy.id,
            name=payload.name,
            price=payload.price,
            sku=payload.sku,
            initial_quantity=payload.initial_quantity,
        )

        # ensure inventory is loaded
        await db.refresh(product, attribute_names=["inventory"])

        await db.commit()

    except Exception:
        await db.rollback()
        raise

    return ProductResponse(
        success=True,
        message=Messages.PRODUCT_CREATED,
        product=product,
    )
