from fastapi import APIRouter
from app.api.v1.routers import health, auth, pharmacies

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(auth.router)
api_router.include_router(pharmacies.router)