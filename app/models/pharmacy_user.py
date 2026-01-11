import enum
import sqlalchemy as sa
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import BaseModel

class PharmacyRole(str, enum.Enum):
    OWNER = "owner"
    STAFF = "staff"
    CLIENT = "client"

class PharmacyUser(BaseModel):
    __tablename__ = "pharmacy_users"

    user_id: Mapped[str] = mapped_column(
        sa.UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    pharmacy_id: Mapped[str] = mapped_column(
        sa.UUID(as_uuid=True),
        ForeignKey("pharmacies.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    role: Mapped[PharmacyRole] = mapped_column(
        sa.Enum(PharmacyRole),
        nullable=False,
    )

    user: Mapped["User"] = relationship(back_populates="pharmacies") # type: ignore
    pharmacy: Mapped["Pharmacy"] = relationship(back_populates="members") # type: ignore

    __table_args__ = (
        sa.UniqueConstraint("user_id", "pharmacy_id", name="uq_user_pharmacy"),
    )
