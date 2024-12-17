from src.models.user import UserModel
from src.schemas.user import UserCreateSchema
from src.utils.service import BaseService
from src.utils.unit_of_work import transaction_mode


class UserService(BaseService):
    base_repository = "user"

    @transaction_mode
    async def get_user_by_email(self, email: str) -> UserModel:
        user: UserModel = await self.uow.user.get_by_query_one_or_none(email=email)
        return user

    @transaction_mode
    async def create_user(self, user: UserCreateSchema, company_id: int = None) -> UserModel:
        return await self.uow.user.add_one_and_get_object(**user.model_dump(), company_id=company_id)
