from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.pharmacy import Pharmacy
from app.models.pharmacy_user import PharmacyRole, PharmacyUser



class PharmacyService:
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_pharmacy(
        self,
        *,
        name: str,
        address: str,
        owner_id
    ) -> Pharmacy:
        pharmacy = Pharmacy(
            name=name,
            address=address
        )
        self.db.add(pharmacy)
        await self.db.flush()
        
        membership = PharmacyUser(
            user_id=owner_id,
            pharmacy_id=pharmacy.id,
            role=PharmacyRole.OWNER
        )
        
        self.db.add(membership)
        
        return pharmacy
    
    async def list_user_pharmacies(
        self,
        user_id
    ):
        result = await self.db.execute(
            select(
                Pharmacy.id,
                Pharmacy.name,
                Pharmacy.address,
                PharmacyUser.role,
            )
            .join(
                PharmacyUser,
                PharmacyUser.pharmacy_id == Pharmacy.id
            )
            .where(
                PharmacyUser.user_id == user_id
            )
            .order_by(Pharmacy.name)
        )
        
        return result.all()