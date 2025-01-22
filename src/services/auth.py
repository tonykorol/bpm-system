from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette.status import HTTP_401_UNAUTHORIZED

from src.models import UserModel
from src.schemas.auth import TokenPayload
from src.services.utils.auth import verify_password
from src.services.utils.jwt import decode_jwt, encode_jwt
from src.utils.service import BaseService
from src.utils.unit_of_work import transaction_mode


class AuthService(BaseService):
    """Service class for handling authentication-related operations.
    """

    base_repository = "auth"

    @transaction_mode
    async def authenticate_user(self, email: str, password: str) -> UserModel | None:
        """Authenticate a user using their email and password.

        Args:
            email (str): The email of the user.
            password (str): The plaintext password of the user.

        Returns:
            UserModel | None: The user object if authentication is successful, otherwise None.

        """
        user = await self.uow.user.get_by_query_one_or_none(email=email)
        if user and verify_password(password, user.password.encode("utf-8")):
            return user
        return None

    @staticmethod
    async def create_token_for_user(user: UserModel) -> str:
        """Generate a JWT token for a given user.

        Args:
            user (UserModel): The user object containing user details.

        Returns:
            str: The generated JWT token.

        """
        payload: dict = {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "company_id": user.company_id,
            "role": user.role.name,
            "department_id": user.department_id,
        }
        token = encode_jwt(payload)
        return token


oauth2_scheme = HTTPBearer()


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme)) -> TokenPayload:
    """Retrieve the current user based on the provided authorization credentials.

    Args:
        credentials (HTTPAuthorizationCredentials): The bearer token credentials.

    Returns:
        TokenPayload: The decoded token payload containing user information.

    Raises:
        HTTPException: If the token is invalid or cannot be decoded.

    """
    token = credentials.credentials
    try:
        payload: TokenPayload = TokenPayload.model_validate(decode_jwt(token))
        return payload
    except ValueError as e:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
