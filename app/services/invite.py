import secrets
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.pharmacy_invite import PharmacyInvite
from app.models.pharmacy_user import PharmacyRole, PharmacyUser

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
    
    async def get_invite_by_token(
        self,
        token: str
    ) -> PharmacyInvite:
        result = await self.db.execute(
            select(PharmacyInvite)
            .where(PharmacyInvite.token == token)
        )
        return result.scalar_one_or_none()
    
    async def accept_invite(
        self,
        *,
        invite: PharmacyInvite,
        user_id,
    ):
        membership = PharmacyUser(
            user_id=user_id,
            pharmacy_id=invite.pharmacy_id,
            role=invite.role
        )
        self.db.add(membership)
        
        invite.accepted = True
        invite.updated_at = datetime.now(timezone.utc)
        
        await self.db.flush()