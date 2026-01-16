import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from uuid import UUID

from app.db.base import BaseModel




class Inventory(BaseModel):
    __tablename__ = "inventories"
    
    product_id: Mapped[UUID] = mapped_column(
        sa.UUID(as_uuid=True),
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )
    
    quantity: Mapped[int] = mapped_column(
        sa.Integer,
        nullable=False,
        default=0,
    )
    
    product: Mapped["Product"] = relationship(# type: ignore
        back_populates="inventory",
    )