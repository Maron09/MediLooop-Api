from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from datetime import datetime, timezone

from app.api.deps import get_db, get_current_user, get_invite_service
from app.schemas.invites import InviteAccept, InviteResponse
from app.services.invite import InviteService
from app.errors.errors import ErrorMessages
from app.messages.messages import Messages



router = APIRouter(prefix="/invites", tags=["Invites"])



@router.post("/accept", response_model=InviteResponse, status_code=status.HTTP_200_OK)
async def accept_invite(
    payload: InviteAccept,
    db: AsyncSession =Depends(get_db),
    user=Depends(get_current_user),
    invite_service: InviteService = Depends(get_invite_service)
): 
    invite = await invite_service.get_invite_by_token(payload.token)
    if not invite:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorMessages.ERR_INVITE_NOT_FOUND
        )
    if invite.accepted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorMessages.ERR_INVITE_NOT_FOUND
        )
    if invite.expires_at < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorMessages.ERR_INVITE_NOT_FOUND
        )
    if invite.email != user.email:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=ErrorMessages.ERR_INVITE_EMAIL_MISMATCH,
        )

    
    await invite_service.accept_invite(
        invite=invite,
        user_id=user.id,
    )
    
    await db.commit()

    return InviteResponse(
        success=True,
        message=Messages.INVITE_ACCEPTED,
    )