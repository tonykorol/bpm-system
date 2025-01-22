from fastapi import HTTPException
from sqlalchemy.util import await_only
from starlette.status import HTTP_400_BAD_REQUEST

from src.models import PositionModel, DepartmentModel, CompanyModel
from src.schemas.auth import TokenPayload
from src.schemas.position import PositionCreateRequest
from src.utils.service import BaseService
from src.utils.unit_of_work import transaction_mode


class PositionService(BaseService):
    base_repository = 'position'

    @transaction_mode
    async def check_user_in_requested_company(self, user_id: int, position_id: int):
        return await self.uow.position.check_user_in_requested_company(user_id, position_id)


    @transaction_mode
    async def check_user_dep_head(self, user_id: int, dep_id: int) -> None:
        department: DepartmentModel = await self.uow.department.get_by_query_one_or_none(id=dep_id)
        if department.head_id != user_id:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="User must be department head")


    @transaction_mode
    async def create_position(self, current_user: TokenPayload, new_position_data: PositionCreateRequest) -> PositionModel:
        await self.check_user_dep_head(user_id=current_user.id, dep_id=current_user.department_id)

        position: PositionModel = await self.uow.position.add_one_and_get_object(
            name=new_position_data.name,
            department_id=current_user.department_id,
        )
        return position


    @transaction_mode
    async def assign_user_to_position(self, user_id: int, position_id: int):
        if not await self.check_user_in_requested_company(user_id, position_id):
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="User must be in company")
        # await self.uow.position.update_one_by_id(user_id, position_id=position_id)