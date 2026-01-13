import datetime
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

from app.db.base import BaseModel
from app.models.pharmacy_user import PharmacyRole


class PharmacyInvite(BaseModel):
    __tablename__ = "pharmacy_invites"
    
    
    pharmacy_id: Mapped[str] = mapped_column(
        sa.UUID(as_uuid=True),
        ForeignKey("pharmacies.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    email: Mapped[str] = mapped_column(
        sa.String(255),
        nullable=False,
        index=True
    )
    
    role: Mapped[str] = mapped_column(
        sa.String(64),
        unique=True,
        nullable=False,
        index=True
    )
    
    token: Mapped[str] = mapped_column(
        sa.String(64),
        unique=True,
        nullable=False,
        index=True
    )
    
    expires_at: Mapped[datetime.datetime] = mapped_column(
        sa.DateTime(timezone=True),
        nullable=False,
    )

    accepted: Mapped[bool] = mapped_column(
        sa.Boolean(),
        default=False,
        nullable=False,
    )