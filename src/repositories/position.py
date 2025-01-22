from typing import TYPE_CHECKING

from sqlalchemy import select

from src.models import PositionModel, UserModel, DepartmentModel
from src.utils.repository import SqlAlchemyRepository

if TYPE_CHECKING:
    from sqlalchemy import Select, Result


class PositionRepository(SqlAlchemyRepository):
    model = PositionModel

    async def check_user_in_requested_company(self, user_id: int, position_id: int) -> bool:
        query: Select = (
            select(UserModel.id)
            .join(PositionModel, PositionModel.id == position_id)
            .join(DepartmentModel, PositionModel.department_id == DepartmentModel.id)
            .where(
                UserModel.id == user_id,
                UserModel.company_id == DepartmentModel.company_id
            )
        )
        result: Result = await self.session.execute(query)
        user = await result.scalar_one()
        return user is not None
