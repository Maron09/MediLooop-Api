# Import models so Alembic can detect them
from app.models.user import User
from app.models.pharmacy import Pharmacy
from app.models.pharmacy_user import PharmacyUser
from app.models.product import Product
from app.models.inventory import Inventory
from app.models.pharmacy_invite import PharmacyInvite

__all__ = [
    "User",
    "Pharmacy",
    "PharmacyUser",
    "Product",
    "Inventory",
    "PharmacyInvite",
]
