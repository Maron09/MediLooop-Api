import secrets
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.pharmacy_invite import PharmacyInvite
from app.models.pharmacy_user import PharmacyRole

from app.core.config import settings


INVITE_EXPIRY_DAYS = settings.INVITE_EXPIRY_DAYS


class InviteService:
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    
    async def create_invite(
        self,
        *,
        pharmacy_id,
        email: str,
        role: PharmacyRole,
    ) -> PharmacyInvite:
        token = secrets.token_urlsafe(32)
        
        invite = PharmacyInvite(
            pharmacy_id= pharmacy_id,
            email=email,
            role=role,
            token=token,
            expires_at=datetime.now(timezone.utc) + timedelta(days=INVITE_EXPIRY_DAYS)
        )
        
        self.db.add(invite)
        await self.db.flush()
        
        return invite