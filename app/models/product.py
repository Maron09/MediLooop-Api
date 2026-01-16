import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from uuid import UUID
from decimal import Decimal

from app.db.base import BaseModel



class Product(BaseModel):
    __tablename__ = "products"
    
    pharmacy_id: Mapped[UUID] = mapped_column(
        sa.UUID(as_uuid=True),
        ForeignKey("pharmacies.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    
    name: Mapped[str] = mapped_column(
        sa.String(length=255),
        nullable=False,
    )
    
    sku: Mapped[str] = mapped_column(
        sa.String(100),
        nullable=False,
    )
    
    price: Mapped[Decimal] = mapped_column(
        sa.Numeric(10, 2),
        nullable=False,
    )
    
    pharmacy: Mapped["Pharmacy"] = relationship(# type: ignore
        back_populates="products",
    )
    
    inventory: Mapped["Inventory"] = relationship(# type: ignore
        back_populates="product",
        uselist=False,
        cascade="all, delete-orphan",
    )
    
    __table_args__ = (
        sa.UniqueConstraint(
            "pharmacy_id",
            "name",
            name="uq_product_pharmacy_name"
        ),
    )