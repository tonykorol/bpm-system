from fastapi import APIRouter

from src.api.v1.routers.auth import router as user_router

router = APIRouter()
router.include_router(user_router, prefix="/v1")
