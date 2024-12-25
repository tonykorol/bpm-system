from fastapi import APIRouter, Depends
from starlette.status import HTTP_201_CREATED, HTTP_200_OK

from src.models import UserModel
from src.schemas.user import UserCreateWithoutPasswordRequest, UserCreateWithoutPasswordResponse, \
    UserSetPasswordRequest, UserSetPasswordResponse
from src.services.user import UserService

router = APIRouter(prefix="/user", tags=["user"])

@router.post(
    path="/create-user",
    status_code=HTTP_201_CREATED,
    response_model=UserCreateWithoutPasswordResponse
)
async def create_user_without_password(
        user: UserCreateWithoutPasswordRequest,
        service: UserService = Depends(UserService),
):
    user: UserModel = await service.create_user_without_password(user)
    return UserCreateWithoutPasswordResponse(payload=user.to_pydantic_schema())


@router.patch(
    path="/set-password",
    status_code=HTTP_200_OK,
    response_model=UserSetPasswordResponse
)
async def set_user_password(
        credentials: UserSetPasswordRequest,
        service: UserService = Depends(UserService),
):
    user: UserModel = await service.set_user_password(credentials)
    return UserSetPasswordResponse(payload=user.to_pydantic_schema())
