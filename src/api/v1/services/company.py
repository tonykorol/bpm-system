from src.models.company import CompanyModel
from src.schemas.company import CompanyCreateSchema
from src.utils.service import BaseService
from src.utils.unit_of_work import transaction_mode


class CompanyService(BaseService):
    base_repository = "company"

    @transaction_mode
    async def create_company(self, company: CompanyCreateSchema) -> CompanyModel:
        return await self.uow.company.add_one_and_get_object(**company.model_dump())
