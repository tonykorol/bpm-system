from sqlalchemy import Insert, exists, insert, select

from src.models import CompanyModel, DepartmentModel, PositionModel, UserModel
from src.models.position import UserPosition
from src.utils.repository import SqlAlchemyRepository


class PositionRepository(SqlAlchemyRepository):
    """Repository class for managing position data and user assignments to positions.

    This class provides methods for checking if a user is associated with a company
    and position, as well as assigning users to positions.
    """

    model = PositionModel

    async def check_user_in_company(self, user_id: int, position_id: id) -> bool:
        """Check if a user is assigned to a specific position within the company.

        Args:
            user_id (int): The ID of the user.
            position_id (int): The ID of the position to check.

        Returns:
            bool: True if the user is in the specified position within the company, False otherwise.

        This method checks if the given user is linked to the provided position, as well as
        verifying the user's affiliation with the company through the position and department associations.

        """
        query = select(
            exists().where(
                UserModel.id == user_id,
                UserPosition.user_id == user_id,
                UserPosition.position_id == position_id,
                PositionModel.id == position_id,
                PositionModel.department_id == DepartmentModel.id,
                DepartmentModel.company_id == CompanyModel.id,
            ),
        )

        result = await self.session.execute(query)
        return result.scalar()

    async def assign_user_to_position(self, user_id: int, position_id: int):
        """Assign a user to a specific position.

        Args:
            user_id (int): The ID of the user to assign.
            position_id (int): The ID of the position to assign the user to.

        This method inserts a record into the UserPosition table, linking the user to the position.

        """
        query: Insert = (
            insert(UserPosition)
            .values(
                user_id=user_id,
                position_id=position_id,
            )
        )
        await self.session.execute(query)
