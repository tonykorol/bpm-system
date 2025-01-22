from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from src.models import DepartmentModel
from src.schemas.department import DepartmentCreateRequest, DepartmentSetHeadRequest, DepartmentUpdateRequest
from src.utils.service import BaseService
from src.utils.unit_of_work import transaction_mode


class DepartmentService(BaseService):
    base_repository = "department"

    @transaction_mode
    async def check_department_has_child(self, department: DepartmentModel) -> bool:
        return await self.uow.department.check_department_has_child(department)

    @transaction_mode
    async def create_department(self, department_data: DepartmentCreateRequest) -> DepartmentModel:
        # try:
        new_department: DepartmentModel = await self.uow.department.create_department(department_data)
        # except Exception as e:
        #     raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=e)
        return new_department

    @transaction_mode
    async def get_department_by_id(self, dep_id: int) -> DepartmentModel:
        department: DepartmentModel = await self.uow.department.get_by_query_one_or_none(id=dep_id)
        if not department:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Invalid department id")
        return department

    @transaction_mode
    async def update_department(self, dep_id: int, department_data: DepartmentUpdateRequest) -> DepartmentModel:
        await self.get_department_by_id(dep_id)
        updated_department: DepartmentModel = await self.uow.department.update_one_by_id(
            dep_id,
            **department_data.model_dump(),
        )
        return updated_department

    @transaction_mode
    async def delete_department(self, dep_id: int) -> bool:
        department: DepartmentModel = await self.get_department_by_id(dep_id)
        if await self.check_department_has_child(department):
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="The department cannot be deleted because it has child departments")
        await self.uow.department.delete_one_by_id(dep_id)
        return True

    @transaction_mode
    async def check_department_has_head(self, department: DepartmentModel) -> bool:
        return bool(department.head_id)

    @transaction_mode
    async def check_user_in_department(self, department_id: int, user_id: int) -> bool:
        return await self.uow.department.check_user_in_department(department_id, user_id)

    @transaction_mode
    async def set_department_head(self, payload: DepartmentSetHeadRequest) -> DepartmentModel:
        department: DepartmentModel = await self.get_department_by_id(payload.department_id)

        if await self.check_department_has_head:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Department already has head user")

        if await self.check_user_in_department(payload.department_id, payload.user_id):
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="The user must be in the department")

        updated_department: DepartmentModel = await self.uow.department.set_department_head(
            department,
            payload.user_id,
        )
        return updated_department
