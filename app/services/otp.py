from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.email_otp import EmailOTP
from app.models.user import User
from app.utils.modules import generate_otp
from app.errors.errors import ErrorMessages



# async def create_email_otp(
#     db: AsyncSession,
#     user_id,
# ) -> EmailOTP:
#     otp = generate_otp()
    
#     record= EmailOTP(
#         user_id=user_id,
#         otp_code=otp,
#         expires_at=datetime.now(timezone.utc) + timedelta(minutes=10),
#     )
#     db.add(record)
#     await db.flush()
#     return record


# async def get_otp_record(db: AsyncSession, otp_code: str) -> EmailOTP | None:
#     """
#     Retrieve the most recent unused OTP record by OTP code.
    
#     Args:
#         db: Database session
#         otp_code: The OTP code to search for
        
#     Returns:
#         EmailOTP record or None if not found
#     """
#     result = await db.execute(
#         select(EmailOTP)
#         .join(User)
#         .where(
#             EmailOTP.otp_code == otp_code,
#             EmailOTP.is_used == False,
#         )
#         .order_by(EmailOTP.created_at.desc())
#     )
#     return result.scalar_one_or_none

# async def activate_user_from_otp(db: AsyncSession, otp_record: EmailOTP) -> User:
#     """
#     Activate user account and mark OTP as used.
    
#     Args:
#         db: Database session
#         otp_record: The OTP record to mark as used
        
#     Returns:
#         The activated User object
#     """
#     user = await db.get(User, otp_record.user_id)
#     user.is_active = True
#     otp_record.is_used = True
#     await db.flush()
#     return user


class OTPService:
    """Service for handling OTP Operations"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_email_otp(self, user_id) -> EmailOTP:
        otp = generate_otp()
        
        record= EmailOTP(
            user_id=user_id,
            otp_code=otp,
            expires_at=datetime.now(timezone.utc) + timedelta(minutes=10),
        )
        self.db.add(record)
        await self.db.flush()
        return record
    
    async def get_otp_record(self, otp_code: str) -> EmailOTP | None:
        """
        Retrieve the most recent unused OTP record by OTP code.
        
        Args:
            otp_code: The OTP code to search for
            
        Returns:
            EmailOTP record or None if not found
        """
        
        result = await self.db.execute(
            select(EmailOTP)
            .join(User)
            .where(
                EmailOTP.otp_code == otp_code,
                EmailOTP.is_used == False
            )
            .order_by(EmailOTP.created_at.desc())
        )
        return result.scalar_one_or_none()
    
    async def activate_user_from_otp(self, otp_record: EmailOTP) -> User:
        """
        Activate user account and mark OTP as used.
        
        Args:
            otp_record: The OTP record to mark as used
            
        Returns:
            The activated User object
        """
        
        user = await self.db.get(User, otp_record.user_id)
        user.is_active = True
        otp_record.is_used = True
        await self.db.flush()
        return user
    
    async def request_new_otp(self, email: str) -> EmailOTP:
        """
        Request a new OTP for a user by email.
        Invalidates all previous unused OTPs for this user.
        
        Args:
            email: User's email address
            
        Returns:
            The new EmailOTP record
            
        Raises:
            ValueError: If user not found
        """
        result = await self.db.execute(
            select(User)
            .where(User.email == email)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            raise ValueError(ErrorMessages.ERR_COULD_NOT_VALIDATE)
        await self.db.execute(
            select(EmailOTP)
            .where(
                EmailOTP.user_id == user.id,
                EmailOTP.is_used == False
            )
        )
        previous_otps = (await self.db.execute(
            select(EmailOTP)
            .where(
                EmailOTP.user_id == user.id,
                EmailOTP.is_used == False,
            )
        )).scalars().all()
        
        for otp in previous_otps:
            otp.is_used = True
        
        new_otp = await self.create_email_otp(user.id)
        await self.db.flush()
        
        return new_otp