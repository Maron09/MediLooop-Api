from fastapi import Depends, HTTPException, status
from app.core.context import PharmacyContext
from app.models.pharmacy_user import PharmacyRole

from app.errors.errors import ErrorMessages
from app.api.deps import get_pharmacy_context


def require_pharmacy_roles(*allowed_roles: PharmacyRole):
    def dependency(
        ctx: PharmacyContext = Depends(get_pharmacy_context),
    ) -> PharmacyContext:
        if ctx.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=ErrorMessages.ERR_PERMISSION_DENIED
            )
        return ctx
    return dependency


def can_invite(inviter_role: PharmacyRole, invited_role: PharmacyRole) -> bool:
    if inviter_role == PharmacyRole.OWNER:
        return True
    if inviter_role == PharmacyRole.STAFF:
        return invited_role == PharmacyRole.CLIENT
    return False


require_owner = require_pharmacy_roles(PharmacyRole.OWNER)

require_owner_or_staff = require_pharmacy_roles(PharmacyRole.OWNER, PharmacyRole.STAFF)

require_any_member = require_pharmacy_roles(
    PharmacyRole.OWNER,
    PharmacyRole.STAFF,
    PharmacyRole.CLIENT,
)