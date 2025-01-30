__all__ = [
    "auth_router",
    "company_router",
    "department_router",
    "position_router",
    "user_router",
]

from src.api.v1.routers.auth import router as auth_router
from src.api.v1.routers.company import router as company_router
from src.api.v1.routers.department import router as department_router
from src.api.v1.routers.position import router as position_router
from src.api.v1.routers.user import router as user_router
