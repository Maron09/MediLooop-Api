from pydantic import BaseModel, Field
from app.models.pharmacy_user import PharmacyRole

class PharmacyCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=255)
    address: str = Field(..., min_length=5, max_length=500)



class PharmacyData(BaseModel):
    id: str
    name: str
    address: str

class PharmacyResponse(BaseModel):
    success: bool
    message: str
    data: PharmacyData


class MyPharmacyItem(BaseModel):
    id: str
    name: str
    address: str
    role: PharmacyRole


class MyPharmaciesResponse(BaseModel):
    succes: bool
    data: list[MyPharmacyItem]