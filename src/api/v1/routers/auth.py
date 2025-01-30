from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_500_INTERNAL_SERVER_ERROR

from src.config import settings
from src.models import UserModel
from src.schemas.auth import AccessTokenScema
from src.services.auth import AuthService, get_auth_service
import logging


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    path="/login",
    description="Authenticate a user using OAuth2. "
                "Upon successful authentication, returns an access token. "
                "The request should include the username and password in the body.",
)
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        service: AuthService = Depends(get_auth_service),
):
    user: UserModel = await service.authenticate_user(form_data.username, form_data.password)
    if not user:
        logger.warning(
            f"Неудачная попытка аутентификации: username={form_data.username}"
        )
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        token = await service.create_token_for_user(user)
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the token. Please try again later.",
        )
    return AccessTokenScema(token=token, token_type=settings.BEARER_TOKEN_TYPE)
