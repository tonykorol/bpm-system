from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from src.models import DepartmentModel
from src.schemas.department import DepartmentCreateRequest, DepartmentSetHeadRequest, DepartmentUpdateRequest
from src.utils.service import BaseService
from src.utils.unit_of_work import transaction_mode


class DepartmentService(BaseService):
    """Service class for managing department-related operations.
    """

    base_repository = "department"

    @transaction_mode
    async def check_department_has_child(self, department: DepartmentModel) -> bool:
        """Check if a department has child departments.

        Args:
            department (DepartmentModel): The department to check.

        Returns:
            bool: True if the department has child departments, False otherwise.

        """
        return await self.uow.department.check_department_has_child(department)

    @transaction_mode
    async def create_department(self, department_data: DepartmentCreateRequest) -> DepartmentModel:
        """Create a new department.

        Args:
            department_data (DepartmentCreateRequest): The data required to create a department.

        Returns:
            DepartmentModel: The newly created department object.

        """
        new_department: DepartmentModel = await self.uow.department.create_department(department_data)
        return new_department

    @transaction_mode
    async def get_department_by_id(self, dep_id: int) -> DepartmentModel:
        """Retrieve a department by its ID.

        Args:
            dep_id (int): The ID of the department.

        Returns:
            DepartmentModel: The department object if found.

        Raises:
            HTTPException: If the department is not found.

        """
        department: DepartmentModel = await self.uow.department.get_by_query_one_or_none(id=dep_id)
        if not department:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Invalid department id")
        return department

    @transaction_mode
    async def update_department(self, dep_id: int, department_data: DepartmentUpdateRequest) -> DepartmentModel:
        """Update a department's details.

        Args:
            dep_id (int): The ID of the department.
            department_data (DepartmentUpdateRequest): The updated department data.

        Returns:
            DepartmentModel: The updated department object.

        """
        await self.get_department_by_id(dep_id)
        updated_department: DepartmentModel = await self.uow.department.update_one_by_id(
            dep_id,
            **department_data.model_dump(),
        )
        return updated_department

    @transaction_mode
    async def delete_department(self, dep_id: int) -> bool:
        """Delete a department by its ID.

        Args:
            dep_id (int): The ID of the department.

        Returns:
            bool: True if the department was successfully deleted.

        Raises:
            HTTPException: If the department has child departments and cannot be deleted.

        """
        department: DepartmentModel = await self.get_department_by_id(dep_id)
        if await self.check_department_has_child(department):
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="The department cannot be deleted because it has child departments")
        await self.uow.department.delete_one_by_id(dep_id)
        return True

    @transaction_mode
    async def check_department_has_head(self, department: DepartmentModel) -> bool:
        """Check if a department already has a head assigned.

        Args:
            department (DepartmentModel): The department to check.

        Returns:
            bool: True if the department has a head, False otherwise.

        """
        return bool(department.head_id)

    @transaction_mode
    async def check_user_in_department(self, department_id: int, user_id: int) -> bool:
        """Check if a user belongs to a specific department.

        Args:
            department_id (int): The ID of the department.
            user_id (int): The ID of the user.

        Returns:
            bool: True if the user is in the department, False otherwise.

        """
        return await self.uow.department.check_user_in_department(department_id, user_id)

    @transaction_mode
    async def set_department_head(self, payload: DepartmentSetHeadRequest) -> DepartmentModel:
        """Assign a head to a department.

        Args:
            payload (DepartmentSetHeadRequest): The request containing department ID and user ID.

        Returns:
            DepartmentModel: The updated department object with the new head assigned.

        Raises:
            HTTPException: If the department already has a head or the user is not part of the department.

        """
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
