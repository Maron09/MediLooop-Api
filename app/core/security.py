from datetime import datetime, timedelta
from typing import Any

from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    normalized = password.encode("utf-8")[:72]
    return pwd_context.hash(normalized)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    normalized = plain_password.encode("utf-8")[:72]
    return pwd_context.verify(normalized, hashed_password)

def create_access_token(subject: str | Any) -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )
    return encoded_jwt