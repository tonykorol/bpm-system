from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette.status import HTTP_401_UNAUTHORIZED

from src.models import UserModel
from src.schemas.auth import AccessTokenScema
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    path="/login",
)
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        service: AuthService = Depends(AuthService),
):
    user: UserModel = await service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = await service.create_token_for_user(user)
    return AccessTokenScema(token=token, token_type="Bearer")
