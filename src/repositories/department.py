from typing import TYPE_CHECKING

from sqlalchemy import exists, select
from sqlalchemy_utils import Ltree, LtreeType

from src.models import DepartmentModel, UserModel
from src.schemas.department import DepartmentCreateRequest
from src.utils.repository import SqlAlchemyRepository

if TYPE_CHECKING:
    from sqlalchemy import Select


class DepartmentRepository(SqlAlchemyRepository):
    """Repository class for managing department data, interacting with the database via SQLAlchemy.

    This class provides methods for creating departments, checking relationships between
    departments and users, and manipulating department paths.
    """

    model = DepartmentModel

    async def create_department(self, department: DepartmentCreateRequest) -> DepartmentModel:
        """Create a new department in the database.

        Args:
            department (DepartmentCreateRequest): The data required to create the department.

        Returns:
            DepartmentModel: The created department object.

        This method generates a department path and stores the department along with its parent and company associations.

        """
        path = await self.generate_department_path(department)
        department: DepartmentModel = await self.add_one_and_get_object(
            name=department.name,
            path=path,
            company_id=department.company_id,
            parent_department_id=department.parent_department_id,
        )
        return department

    async def generate_department_path(self, department: DepartmentCreateRequest) -> LtreeType:
        """Generate the path for a department based on its parent.

        Args:
            department (DepartmentCreateRequest): The department data.

        Returns:
            LtreeType: The generated path for the department, using the Ltree type.

        If the department has a parent, the parent’s path is used to construct the new path.
        Otherwise, the department name is used as the path.

        """
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
        """Check if a department has any child departments.

        Args:
            department (DepartmentModel): The department to check.

        Returns:
            bool: True if the department has children, False otherwise.

        This method checks if there are any departments whose path is a descendant of the given department's path.

        """
        query: Select = select(
            exists().where(
                DepartmentModel.path.descendant_of(department.path),
                DepartmentModel.path != department.path,
            ),
        )
        return await self.session.scalars(query)

    async def check_user_in_department(self, user_id: int, department_id: int) -> bool:
        """Check if a user is assigned to a specific department.

        Args:
            user_id (int): The ID of the user.
            department_id (int): The ID of the department.

        Returns:
            bool: True if the user is assigned to the department, False otherwise.

        """
        query = select(
            exists().where(
                UserModel.department_id == department_id,
                UserModel.id == user_id,
            ),
        )
        return await self.session.scalar(query)

    async def set_department_head(self, department: DepartmentModel, head_id: int) -> DepartmentModel:
        """Set the head of a department.

        Args:
            department (DepartmentModel): The department to update.
            head_id (int): The user ID to set as the department head.

        Returns:
            DepartmentModel: The updated department with the new head.

        This method updates the department with the provided head user ID.

        """
        department: DepartmentModel = await self.update_one_by_id(
            department.id,
            head_id=head_id,
        )
        return department
