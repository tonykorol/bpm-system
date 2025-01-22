from sqlalchemy import select, exists, Insert, insert

from src.models import PositionModel, UserModel, DepartmentModel, CompanyModel
from src.models.position import UserPosition
from src.utils.repository import SqlAlchemyRepository


class PositionRepository(SqlAlchemyRepository):
    model = PositionModel

    async def check_user_in_company(self, user_id: int, position_id: id) -> bool:
        query = select(
            exists().where(
                UserModel.id == user_id,
                UserPosition.user_id == user_id,
                UserPosition.position_id == position_id,
                PositionModel.id == position_id,
                PositionModel.department_id == DepartmentModel.id,
                DepartmentModel.company_id == CompanyModel.id
            )
        )

        result = await self.session.execute(query)
        return result.scalar()


    async def assign_user_to_position(self, user_id: int, position_id: int):
        query: Insert = (
            insert(UserPosition)
            .values(
                user_id=user_id,
                position_id=position_id
            )
        )
        await self.session.execute(query)
