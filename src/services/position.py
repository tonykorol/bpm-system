from fastapi import HTTPException
from starlette.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST

from src.models import PositionModel
from src.schemas.position import PositionCreateRequest, PositionUpdateRequest, PositionAssignRequest
from src.utils.service import BaseService
from src.utils.unit_of_work import transaction_mode


class PositionService(BaseService):
    base_repository = 'position'

    @transaction_mode
    async def create_position(self, position_data: PositionCreateRequest) -> PositionModel:
        position: PositionModel = await self.uow.position.add_one_and_get_object(**position_data.model_dump())
        return position


    @transaction_mode
    async def get_position_by_id(self, position_id: int) -> PositionModel:
        position: PositionModel = await self.uow.position.get_by_query_one_or_none(id=position_id)
        if not position:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Invalid position id")
        return position


    @transaction_mode
    async def update_position(self, pos_id: int, position_data: PositionUpdateRequest) -> PositionModel:
        updated_position: PositionModel = await self.uow.position.update_one_by_id(
            pos_id,
            **position_data.model_dump()
        )
        return updated_position


    @transaction_mode
    async def delete_position(self, position_id: int) -> bool:
        await self.get_position_by_id(position_id)
        await self.uow.position.delete_one_by_id(position_id)
        return True


    @transaction_mode
    async def check_user_in_company(self, user_id: int, position_id: int) -> bool:
        return await self.uow.position.check_user_in_company(user_id, position_id)


    @transaction_mode
    async def assign_user_to_position(self, payload: PositionAssignRequest) -> PositionModel:
        position: PositionModel = await self.get_position_by_id(payload.position_id)
        if not self.check_user_in_company(payload.user_id, payload.position_id):
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="User must be in requested company")
        await self.uow.position.assign_user_to_position(**payload.model_dump())
        return position
