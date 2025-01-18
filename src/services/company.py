from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

from src.models import CompanyModel
from src.models.user import UserRole, UserModel
from src.schemas.auth import SignUpCompleteRequest
from src.schemas.company import CompanyCreateSchema
from src.schemas.user import UserCreateSchema
from src.services.utils.auth import hash_password
from src.utils.service import BaseService
from src.utils.unit_of_work import transaction_mode

from src.services.invite import InviteService


class CompanyService(BaseService):
    base_repository = "company"

    def __init__(self):
        super().__init__()
        self.invite_service: InviteService = InviteService()

    @transaction_mode
    async def check_email(self, email: str) -> bool:
        account = await self.uow.user.get_by_query_one_or_none(email=email)
        if not account:
            await self.invite_service.create_and_send_invite(email)
            return True
        return False

    @transaction_mode
    async def create_company_and_user(self, payload: SignUpCompleteRequest) -> CompanyModel:
        company_exist = await self.uow.company.get_by_query_one_or_none(name=payload.company_name)
        if company_exist:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail=f"Company with name {payload.company_name} already exists"
            )

        company_data = CompanyCreateSchema(name=payload.company_name)
        company: CompanyModel = await self.uow.company.add_one_and_get_object(**company_data.model_dump())
        user_data = UserCreateSchema(
            first_name=payload.first_name,
            last_name=payload.last_name,
            email=payload.account,
            role=UserRole.COMPANY_ADMIN,
            password=hash_password(payload.password),
            company_id=company.id,
        )
        await self.uow.user.add_one_and_get_object(**user_data.model_dump())
        return company
