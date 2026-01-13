from pydantic import BaseModel, EmailStr
from app.models.pharmacy_user import PharmacyRole


class InviteCreate(BaseModel):
    email: EmailStr
    role: PharmacyRole



class InviteResponse(BaseModel):
    success: bool
    message: str