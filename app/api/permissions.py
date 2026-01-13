from fastapi import Depends, HTTPException, status
from app.core.context import PharmacyContext
from app.models.pharmacy_user import PharmacyRole

from app.errors.errors import ErrorMessages


def reuire_pharmacy_roles(*allowed_roles: PharmacyRole):
    def dependency(
        ctx: PharmacyContext = Depends(),
    ) -> PharmacyContext:
        if ctx.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=ErrorMessages.ERR_INSUFFICIENT_PERMISSIONS
            )
        return ctx
    return dependency


def can_invite(inviter_role: PharmacyRole, invited_role: PharmacyRole) -> bool:
    if inviter_role == PharmacyRole.OWNER:
        return True
    if inviter_role == PharmacyRole.STAFF:
        return invited_role == PharmacyRole.CLIENT
    return False