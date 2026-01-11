import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import BaseModel

class User(BaseModel):
    __tablename__ = "users"
    
    email: Mapped[str] = mapped_column(
        sa.String(length=255),
        unique=True,
        nullable=False,
        index=True,
    )
    first_name: Mapped[str] = mapped_column(
        sa.String(length=100),
        nullable=True,
    )
    last_name: Mapped[str] = mapped_column(
        sa.String(length=100),
        nullable=True,
    )
    hashed_password: Mapped[str] = mapped_column(
        sa.String(length=255),
        nullable=False,
    )
    
    is_active: Mapped[bool] = mapped_column(
        sa.Boolean(),
        default=False,
        nullable=False,
    )
    
    pharmacies: Mapped[list["PharmacyUser"]] = relationship( # type: ignore
        back_populates="user",
        cascade="all, delete-orphan",
    )