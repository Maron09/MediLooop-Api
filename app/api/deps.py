from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.sessions import get_db
from app.models.user import User
from sqlalchemy import select

from app.errors.errors import ErrorMessages
from app.services.otp import OTPService
from app.services.auth import AuthService

oauth_scheme = OAuth2PasswordBearer(tokenUrl=settings.TOKEN_URL)

async def get_current_user(
    token: str = Depends(oauth_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=ErrorMessages.ERR_COULD_NOT_VALIDATE
    )
    
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        user_id: str | None = payload.get("sub")
        if user_id is None:
            raise credential_exception
    except JWTError:
        raise credential_exception
    
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()
    
    if user is None or not user.is_active:
        raise credential_exception
    
    return user

async def get_otp_service(
    db: AsyncSession = Depends(get_db)
) -> OTPService:
    return OTPService(db)

async def get_auth_service(
    db: AsyncSession = Depends(get_db)
) -> AuthService:
    return AuthService(db)