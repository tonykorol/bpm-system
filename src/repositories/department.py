from typing import TYPE_CHECKING

from sqlalchemy import exists, select
from sqlalchemy_utils import Ltree, LtreeType

from src.models import DepartmentModel, UserModel
from src.schemas.department import DepartmentCreateRequest
from src.utils.repository import SqlAlchemyRepository

if TYPE_CHECKING:
    from sqlalchemy import Select


class DepartmentRepository(SqlAlchemyRepository):
    model = DepartmentModel

    async def create_department(self, department: DepartmentCreateRequest) -> DepartmentModel:
        path = await self.generate_department_path(department)
        department: DepartmentModel = await self.add_one_and_get_object(
            name=department.name,
            path=path,
            company_id=department.company_id,
            parent_department_id=department.parent_department_id,
        )
        return department

    async def generate_department_path(self, department: DepartmentCreateRequest) -> LtreeType:
        global company_name
        parent_path = None
        department_name = department.name.replace(" ", "_")
        if department.parent_department_id:
            parent: DepartmentModel = await self.get_by_query_one_or_none(
                id=department.parent_department_id,
            )
            parent_path = parent.path
        path = f"{parent_path}.{department_name}" if parent_path else f"{department_name}"
        return Ltree(path)

    async def check_department_has_child(self, department: DepartmentModel) -> bool:
        query: Select = select(
            exists().where(
                DepartmentModel.path.descendant_of(department.path),
                DepartmentModel.path != department.path,
            ),
        )
        return await self.session.scalars(query)

    async def check_user_in_department(self, user_id: int, department_id: int) -> bool:
        query = select(
            exists().where(
                UserModel.department_id == department_id,
                UserModel.id == user_id,
            ),
        )
        return await self.session.scalar(query)

    async def set_department_head(self, department: DepartmentModel, head_id: int) -> DepartmentModel:
        department: DepartmentModel = await self.update_one_by_id(
            department.id,
            head_id=head_id,
        )
        return department
