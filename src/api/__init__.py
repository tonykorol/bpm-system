from fastapi import APIRouter

from src.api.v1.routers import auth_router, company_router, department_router, position_router, user_router

router = APIRouter()
router.include_router(auth_router, prefix="/v1")
router.include_router(user_router, prefix="/v1")
router.include_router(company_router, prefix="/v1")
router.include_router(department_router, prefix="/v1")
router.include_router(position_router, prefix="/v1")
