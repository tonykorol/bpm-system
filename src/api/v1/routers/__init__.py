__all__ = [
    'auth_router',
    'user_router',
]

from src.api.v1.routers.company import router as auth_router
from src.api.v1.routers.user import router as user_router