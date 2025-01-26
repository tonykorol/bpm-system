from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN

from src.models import UserModel
from src.schemas.auth import TokenPayload
from src.schemas.user import UserCreateWithoutPasswordRequest, UserSetPasswordRequest, UserUpdateRequest
from src.services.utils.auth import hash_password
from src.services.utils.email_sender import send_email
from src.utils.service import BaseService
from src.utils.unit_of_work import transaction_mode


class UserService(BaseService):
    """Service class for managing user-related operations such as user creation, password setting, and updating user information.
    """

    base_repository = "user"

    @staticmethod
    async def check_user_is_company_admin(user: TokenPayload) -> bool:
        """Check if the user has the "COMPANY_ADMIN" role.

        Args:
            user (TokenPayload): The current user's token payload.

        Raises:
            HTTPException: If the user does not have the "COMPANY_ADMIN" role.

        """
        if user.role != "COMPANY_ADMIN":
            raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="User must be COMPANY_ADMIN")

    @transaction_mode
    async def create_user_without_password(
            self,
            current_user: TokenPayload,
            user: UserCreateWithoutPasswordRequest,
            company_id: int,
    ) -> UserModel:
        """Create a new user without setting a password and send a set password email.

        Args:
            current_user (TokenPayload): The current authenticated user who must be a COMPANY_ADMIN.
            user (UserCreateWithoutPasswordRequest): The user data to create the new user.
            company_id (int): The company ID to associate the new user with.

        Returns:
            UserModel: The newly created user.

        Raises:
            HTTPException: If the current user is not a COMPANY_ADMIN or the user already exists.

        """
        await self.check_user_is_company_admin(current_user)

        user_exist = await self.repository.get_by_query_one_or_none(email=user.email)
        if user_exist:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="User already exists",
            )

        user: UserModel = await self.repository.add_one_and_get_object(**user.model_dump(), company_id=company_id)

        await self.send_set_password_email(user)

        return user

    @staticmethod
    async def send_set_password_email(user: UserModel) -> None:
        """Send an email to the user to set their password.

        Args:
            user (UserModel): The user to whom the set password email will be sent.

        """
        email_body = 'Для завершения регистрации перейдите по ссылке: "ссылка"'
        send_email(user.email, "Set your password", email_body)

    @transaction_mode
    async def set_user_password(self, credentials: UserSetPasswordRequest) -> UserModel:
        """Set a new password for an existing user.

        Args:
           credentials (UserSetPasswordRequest): The user's email and new password.

        Returns:
           UserModel: The updated user object.

        Raises:
           HTTPException: If the user does not exist.

        """
        user = await self.repository.get_by_query_one_or_none(email=credentials.email)
        if not user:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="User does not exists",
            )
        password = hash_password(credentials.password).decode()
        return await self.repository.update_one_by_id(user.id, password=password)

    @transaction_mode
    async def update_user_info(self, current_user: TokenPayload, update_data: UserUpdateRequest) -> UserModel:
        """Update the user's first name and last name.

        Args:
            current_user (TokenPayload): The current authenticated user.
            update_data (UserUpdateRequest): The data to update the user's information.

        Returns:
            UserModel: The updated user object.

        """
        user: UserModel = await self.repository.get_by_query_one_or_none(email=current_user.email)
        await self.repository.update_one_by_id(user.id, first_name=update_data.first_name, last_name=update_data.last_name)
        return user

    @transaction_mode
    async def set_user_as_department_head(self, user: UserModel, department_id: int) -> None:
        """Set a user as the head of a department.

        Args:
            user (UserModel): The user to set as the department head.
            department_id (int): The department ID to assign the user to as the head.

        """
        user.department_id = department_id
