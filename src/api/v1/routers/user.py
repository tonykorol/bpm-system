from fastapi import APIRouter, Depends
from starlette.status import HTTP_201_CREATED, HTTP_200_OK

from src.models import UserModel
from src.models.user import UserRole
from src.schemas.user import UserCreateWithoutPasswordRequest, UserCreateWithoutPasswordResponse, \
    UserSetPasswordRequest, UserSetPasswordResponse, GetMeResponse, UserUpdateResponse, UserUpdateRequest
from src.services.auth import get_current_user
from src.services.user import UserService

router = APIRouter(prefix="/user", tags=["user"])

@router.post(
    path="/create-user",
    status_code=HTTP_201_CREATED,
    response_model=UserCreateWithoutPasswordResponse
)
async def create_user_without_password(
        new_user: UserCreateWithoutPasswordRequest,
        current_user: dict = Depends(get_current_user),
        service: UserService = Depends(UserService),
):
    if current_user and current_user['role'] == UserRole.COMPANY_ADMIN.name:
        user: UserModel = await service.create_user_without_password(new_user, company_id=current_user['company_id'])
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


@router.get(
    path="/me",
    status_code=HTTP_200_OK,
    response_model=GetMeResponse
)
async def get_me(current_user: dict = Depends(get_current_user)):
    return GetMeResponse.model_validate(current_user)


@router.put(
    path="/me",
    status_code=HTTP_200_OK,
    response_model=UserUpdateResponse,
)
async def update_me(
        update_data: UserUpdateRequest,
        current_user: dict = Depends(get_current_user),
        user_service: UserService = Depends(UserService),
):
    updated_user: UserModel = await user_service.update_user_info(current_user, update_data)
    return UserUpdateResponse(payload=updated_user.to_pydantic_schema())
