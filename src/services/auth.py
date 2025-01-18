from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials
from starlette.status import HTTP_401_UNAUTHORIZED

from src.models import UserModel
from src.services.utils.auth import verify_password
from src.services.utils.jwt import encode_jwt, decode_jwt
from src.utils.service import BaseService
from src.utils.unit_of_work import transaction_mode


class AuthService(BaseService):
    @transaction_mode
    async def authenticate_user(self, email: str, password: str) -> UserModel | None:
        user = await self.uow.user.get_by_query_one_or_none(email=email)
        if user and verify_password(password, user.password.encode("utf-8")):
            return user
        return None

    @staticmethod
    async def create_token_for_user(user: UserModel) -> str:
        payload: dict = {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "company_id": user.company_id,
            "role": user.role.name,
        }
        token = encode_jwt(payload)
        return token


oauth2_scheme = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    token = credentials.credentials
    try:
        payload = decode_jwt(token)
        return payload
    except ValueError as e:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
