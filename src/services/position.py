from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from src.models import PositionModel
from src.schemas.position import PositionAssignRequest, PositionCreateRequest, PositionUpdateRequest
from src.utils.service import BaseService
from src.utils.unit_of_work import transaction_mode


class PositionService(BaseService):
    """Service class for managing positions and assigning users to them.
    """

    base_repository = "position"

    @transaction_mode
    async def create_position(self, position_data: PositionCreateRequest) -> PositionModel:
        """Create a new position.

        Args:
            position_data (PositionCreateRequest): The data required to create a position.

        Returns:
            PositionModel: The newly created position object.

        """
        position: PositionModel = await self.uow.position.add_one_and_get_object(**position_data.model_dump())
        return position

    @transaction_mode
    async def get_position_by_id(self, position_id: int) -> PositionModel:
        """Retrieve a position by its ID.

        Args:
            position_id (int): The ID of the position.

        Returns:
            PositionModel: The position object if found.

        Raises:
            HTTPException: If the position is not found.

        """
        position: PositionModel = await self.uow.position.get_by_query_one_or_none(id=position_id)
        if not position:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Invalid position id")
        return position

    @transaction_mode
    async def update_position(self, pos_id: int, position_data: PositionUpdateRequest) -> PositionModel:
        """Update a position's details.

        Args:
            pos_id (int): The ID of the position to update.
            position_data (PositionUpdateRequest): The updated position data.

        Returns:
            PositionModel: The updated position object.

        """
        updated_position: PositionModel = await self.uow.position.update_one_by_id(
            pos_id,
            **position_data.model_dump(),
        )
        return updated_position

    @transaction_mode
    async def delete_position(self, position_id: int) -> bool:
        """Delete a position by its ID.

        Args:
            position_id (int): The ID of the position to delete.

        Returns:
            bool: True if the position was successfully deleted.

        """
        await self.get_position_by_id(position_id)
        await self.uow.position.delete_one_by_id(position_id)
        return True

    @transaction_mode
    async def check_user_in_company(self, user_id: int, position_id: int) -> bool:
        """Check if a user is part of the company associated with a specific position.

        Args:
            user_id (int): The ID of the user.
            position_id (int): The ID of the position.

        Returns:
            bool: True if the user is in the company associated with the position, False otherwise.

        """
        return await self.uow.position.check_user_in_company(user_id, position_id)

    @transaction_mode
    async def assign_user_to_position(self, payload: PositionAssignRequest) -> PositionModel:
        """Assign a user to a specific position.

        Args:
            payload (PositionAssignRequest): The request containing position ID and user ID.

        Returns:
            PositionModel: The updated position object.

        Raises:
            HTTPException: If the user is not part of the requested company.

        """
        position: PositionModel = await self.get_position_by_id(payload.position_id)
        if not self.check_user_in_company(payload.user_id, payload.position_id):
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="User must be in requested company")
        await self.uow.position.assign_user_to_position(**payload.model_dump())
        return position
