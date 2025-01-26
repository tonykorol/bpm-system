from fastapi import APIRouter, Depends
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from src.models import UserModel
from src.schemas.auth import TokenPayload
from src.schemas.user import (
        GetMeResponse,
        UserCreateWithoutPasswordRequest,
        UserCreateWithoutPasswordResponse,
        UserSetPasswordRequest,
        UserSetPasswordResponse,
        UserUpdateRequest,
        UserUpdateResponse,
)
from src.services.auth import get_current_user
from src.services.user import UserService

router = APIRouter(prefix="/user", tags=["user"])


@router.post(
    path="/create-user",
    status_code=HTTP_201_CREATED,
    response_model=UserCreateWithoutPasswordResponse,
    description="Create a new user without setting a password. Requires user details except for password. "
                "Returns the created user's information.",
)
async def create_user_without_password(
        new_user: UserCreateWithoutPasswordRequest,
        current_user: TokenPayload = Depends(get_current_user),
        service: UserService = Depends(UserService),
):
        user: UserModel = await service.create_user_without_password(current_user, new_user, company_id=current_user.company_id)
        return UserCreateWithoutPasswordResponse(payload=user.to_pydantic_schema())


@router.patch(
    path="/set-password",
    status_code=HTTP_200_OK,
    response_model=UserSetPasswordResponse,
    description="Set or update a user's password. Requires the new password and user credentials. "
                "Returns the updated user's information.",
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
    response_model=GetMeResponse,
    description="Retrieve the currently authenticated user's details. Returns information about the authenticated user.",
)
async def get_me(current_user: TokenPayload = Depends(get_current_user)):
    return GetMeResponse(**current_user.model_dump())


@router.put(
    path="/me",
    status_code=HTTP_200_OK,
    response_model=UserUpdateResponse,
    description="Update the currently authenticated user's information. Requires updated user data. "
                "Returns the updated user details.",
)
async def update_me(
        update_data: UserUpdateRequest,
        current_user: TokenPayload = Depends(get_current_user),
        user_service: UserService = Depends(UserService),
):
    updated_user: UserModel = await user_service.update_user_info(current_user, update_data)
    return UserUpdateResponse(payload=updated_user.to_pydantic_schema())
