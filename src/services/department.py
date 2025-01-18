from fastapi import HTTPException
from sqlalchemy_utils import Ltree
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from src.models import DepartmentModel, CompanyModel, UserModel
from src.repositories.department import DepartmentRepository
from src.schemas.department import DepartmentCreateRequest
from src.utils.service import BaseService
from src.utils.unit_of_work import transaction_mode


class DepartmentService(BaseService):
    base_repository = DepartmentRepository

    @staticmethod
    async def check_user_role(user: dict) -> None:
        if user['role'] != "COMPANY_ADMIN":
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="User must be COMPANY_ADMIN")

    @transaction_mode
    async def create_department(self, department_data: DepartmentCreateRequest, current_user: dict) -> DepartmentModel:
        await self.check_user_role(current_user)

        head_user: UserModel = await self.uow.user.get_by_query_one_or_none(id=department_data.head_id)
        if head_user is None:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Head user does not exists")

        company: CompanyModel = await self.uow.company.get_by_query_one_or_none(id=current_user['company_id'])

        department_path = f"{company.name}.{department_data.name}"

        if isinstance(department_path, str):
            department_path = Ltree(department_path)

        department = await self.uow.department.add_one_and_get_object(
            name=department_data.name,
            path=department_path,
            company_id=company.id,
            head_id=head_user.id
        )
        return department

    @transaction_mode
    async def get_department_by_id(self, department_id: int) -> DepartmentModel:
        department: DepartmentModel = await self.uow.department.get_by_query_one_or_none(id=department_id)
        if department is None:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Invalid department id")
        return department




