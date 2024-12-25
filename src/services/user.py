from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from src.models import UserModel
from src.schemas.user import UserCreateWithoutPasswordRequest, UserSetPasswordRequest
from src.services.utils.email_sender import send_email
from src.services.utils.password import hash_password
from src.utils.service import BaseService
from src.utils.unit_of_work import transaction_mode


class UserService(BaseService):
    base_repository = "user"

    @transaction_mode
    async def create_user_without_password(self, user: UserCreateWithoutPasswordRequest) -> UserModel:
        user_exist = await self.uow.user.get_by_query_one_or_none(email=user.email)
        if user_exist:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="User already exists"
            )

        company_exists = await self.uow.company.get_by_query_one_or_none(id=user.company_id)
        if not company_exists:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="The company does not exist"
            )

        user: UserModel = await self.uow.user.add_one_and_get_object(**user.model_dump())

        await self.send_set_password_email(user)

        return user

    @staticmethod
    async def send_set_password_email(user: UserModel) -> None:
        email_body = f'Для установки пароля перейдите по ссылке: "ссылка"'
        send_email(user.email, "Set your password", email_body)

    @transaction_mode
    async def set_user_password(self, credentials: UserSetPasswordRequest) -> UserModel:
        user = await self.uow.user.get_by_query_one_or_none(email=credentials.email)
        if not user:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="User does not exists"
            )
        password = hash_password(credentials.password).decode()
        return await self.uow.user.update_one_by_id(user.id, password=password)
