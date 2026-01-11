from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.api.deps import get_db
from app.core.security import create_access_token
from app.schemas.auth import Token, UserCreate, RegisterResponse, OTPVerify, OTPResponse, NewOTP
from app.services.auth import AuthService
from app.services.otp import OTPService
from app.api.deps import get_otp_service, get_auth_service
from app.services.email import send_email_otp
from app.messages.messages import Messages
from app.errors.errors import ErrorMessages

from datetime import datetime, timezone


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db),
    otp_service: OTPService = Depends(get_otp_service),
    auth_service: AuthService = Depends(get_auth_service)
):
    try:
        async with db.begin():
            user = await auth_service.create_user(
                email=user_in.email,
                first_name=user_in.first_name,
                last_name=user_in.last_name,
                password=user_in.password,
            )
            otp_record = await otp_service.create_email_otp(user.id)

    except IntegrityError:
        # Transaction is already rolled back automatically
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=ErrorMessages.ERR_USER_EXISTS,
        )

    await send_email_otp(user.email, otp_record.otp_code)

    return RegisterResponse(
        success=True,
        message=Messages.USER_REGISTERED,
    )


@router.post("/verify-otp", response_model=OTPResponse, status_code=status.HTTP_200_OK)
async def verify_otp(
    payload: OTPVerify,
    db: AsyncSession = Depends(get_db),
    otp_service: OTPService = Depends(get_otp_service),
):
    async with db.begin():
        otp_record = await otp_service.get_otp_record(payload.otp_code)

        if not otp_record or otp_record.expires_at < datetime.now(timezone.utc):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorMessages.ERR_OTP_INVALID,
            )

        await otp_service.activate_user_from_otp(otp_record)

    return OTPResponse(
        success=True,
        message=Messages.OTP_VERIFIED,
    )



@router.post("/resend-otp", response_model=OTPResponse, status_code=status.HTTP_200_OK)
async def resend_otp(
    payload: NewOTP,
    db: AsyncSession = Depends(get_db),
    otp_service: OTPService = Depends(get_otp_service)
):
    try:
        async with db.begin():
            otp_record = await otp_service.request_new_otp(payload.email)
        await send_email_otp(payload.email, otp_record.otp_code)
        return OTPResponse(
            success=True,
            message=Messages.OTP_RESENT
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorMessages.ERR_COULD_NOT_VALIDATE
        )


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
    auth_service: AuthService = Depends(get_auth_service)
):
    user = await auth_service.authenticate_user(
        email=form_data.username,
        password=form_data.password
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ErrorMessages.ERR_INVALID_CRED
        )
    token = create_access_token(user.id)
    return Token(
        access_token=token
    )