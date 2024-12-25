from fastapi import APIRouter

from src.api.v1.routers import auth_router
from src.api.v1.routers import user_router

router = APIRouter()
router.include_router(auth_router, prefix="/v1")
router.include_router(user_router, prefix="/v1")
