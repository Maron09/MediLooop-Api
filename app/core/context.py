from dataclasses import dataclass
from app.models.user import User
from app.models.pharmacy import Pharmacy
from app.models.pharmacy_user import PharmacyRole



@dataclass
class PharmacyContext:
    user: User
    pharmacy: Pharmacy
    role: PharmacyRole