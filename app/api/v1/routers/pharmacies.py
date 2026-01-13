from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_pharmacy_service, get_current_user, get_db, get_invite_service, get_pharmacy_context
from app.schemas.pharmacy import PharmacyCreate, PharmacyResponse, PharmacyData, MyPharmaciesResponse, MyPharmacyItem
from app.schemas.invites import InviteCreate, InviteResponse
from app.services.pharmacy import PharmacyService
from app.services.invite import InviteService
from app.messages.messages import Messages
from app.errors.errors import ErrorMessages
from app.api.permissions import can_invite

router = APIRouter(prefix="/pharmacies", tags=["Pharmacies"])



@router.post("", response_model=PharmacyResponse, status_code=status.HTTP_201_CREATED)
async def create_pharmacy_endpoint(
    payload: PharmacyCreate,
    db: AsyncSession = Depends(get_db),
    pharmacy_service: PharmacyService = Depends(get_pharmacy_service),
    user=Depends(get_current_user)
):
    
    pharmacy = await pharmacy_service.create_pharmacy(
        name=payload.name,
        address=payload.address,
        owner_id=user.id
    )
    await db.commit()
    
    return PharmacyResponse(
        success=True,
        message=Messages.PHARMACY_CREATED,
        data=PharmacyData(
            id=str(pharmacy.id),
            name=pharmacy.name,
            address=pharmacy.address,
        )
    )

@router.get("/me", response_model=MyPharmaciesResponse, status_code=status.HTTP_200_OK)
async def list_my_pharmacies(
    user=Depends(get_current_user),
    pharmacy_service: PharmacyService = Depends(get_pharmacy_service)
):
    rows = await pharmacy_service.list_user_pharmacies(user.id)
    
    data = [
        MyPharmacyItem(
            id=str(pharmacy_id),
            name=name,
            address=address,
            role=role
        )
        for pharmacy_id, name, address, role in rows
    ]
    
    return MyPharmaciesResponse(
        succes=True,
        data=data
    )

@router.post("/{pharmacy_id}/invites", response_model=InviteResponse, status_code=status.HTTP_201_CREATED)
async def invite_user(
    payload: InviteCreate,
    db: AsyncSession = Depends(get_db),
    ctx=Depends(get_pharmacy_context),
    invite_service: InviteService = Depends(get_invite_service)
):
    if not can_invite(ctx.role, payload.role):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=ErrorMessages.ERR_INVALID_ROLE
        )
    invite = await invite_service.create_invite(
        pharmacy_id=ctx.pharmacy.id,
        email=payload.email,
        role=payload.role
    )
    await db.commit()
    
    # TODO: send email with invite.token
    print(f"[INVITE] Token: {invite.token}")
    
    return InviteResponse(
        success=True,
        message=Messages.INVITE_SENT
    )
