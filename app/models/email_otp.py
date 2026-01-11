import datetime
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from app.db.base import BaseModel


class EmailOTP(BaseModel):
    __tablename__ = "email_otps"
    
    user_id: Mapped[str] = mapped_column(
        sa.UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    
    otp_code: Mapped[str] = mapped_column(
        sa.String(6),
        nullable=False,
    )
    
    expires_at: Mapped[datetime.datetime] = mapped_column(
        sa.DateTime(timezone=True),
        nullable=False,
    )
    
    is_used: Mapped[bool] = mapped_column(
        sa.Boolean,
        default=False,
        nullable=False,
    )