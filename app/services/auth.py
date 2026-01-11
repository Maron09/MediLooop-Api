from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import User
from app.core.security import hash_password, verify_password


# async def authenticate_user(
#     db: AsyncSession,
#     email: str,
#     password: str,
# ) -> User | None:
#     result = await db.execute(
#         select(User).where(User.email == email)
#     )
#     user = result.scalar_one_or_none()
    
#     if not user:
#         return None
    
#     if not verify_password(password, user.hashed_password):
#         return None
    
#     return user


# async def create_user(
#     db: AsyncSession,
#     email: str,
#     first_name: str,
#     last_name: str,
#     password: str,
# ) -> User:
#     user = User(
#         email=email,
#         first_name=first_name,
#         last_name=last_name,
#         hashed_password=hash_password(password),
#     )
#     db.add(user)
#     await db.flush()
#     return user


class AuthService:
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    
    async def authenticate_user(self, email: str, password: str) -> User | None:
        result = await self.db.execute(
            select(User)
            .where(User.email == email)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            return None
        
        if not verify_password(password, user.hashed_password):
            return None
        
        return user
    
    async def create_user(
        self,
        email: str,
        first_name: str,
        last_name: str,
        password: str,
    ) -> User:
        user = User(
            email=email,
            first_name=first_name,
            last_name=last_name,
            hashed_password=hash_password(password),
        )
        self.db.add(user)
        await self.db.flush()
        return user