import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import BaseModel


class Pharmacy(BaseModel):
    __tablename__ = "pharmacies"
    
    name: Mapped[str] = mapped_column(
        sa.String(length=255),
        nullable=False,
        index=True,
    )
    address: Mapped[str] = mapped_column(
        sa.String(length=500),
        nullable=False,
    )
    
    members: Mapped[list["PharmacyUser"]] = relationship( # type: ignore
        back_populates="pharmacy",
        cascade="all, delete-orphan",
    )
    
    products: Mapped[list["Product"]] = relationship( # type: ignore
        back_populates="pharmacy",
        cascade="all, delete-orphan",
    )