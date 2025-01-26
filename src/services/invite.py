import secrets
import string

from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

from src.models.invite import InviteModel
from src.services.utils.email_sender import send_email
from src.utils.service import BaseService
from src.utils.unit_of_work import transaction_mode


class InviteService(BaseService):
    """Service class for managing invites, including creation, validation, and email sending.
    """

    base_repository = "invite"

    @transaction_mode
    async def get_unused_invite_by_email(self, email: str) -> InviteModel:
        """Retrieve an unused invite by email.

        Args:
            email (str): The email address to search for.

        Returns:
            InviteModel: The unused invite object if found, otherwise None.

        """
        return await self.repository.get_by_query_one_or_none(email=email, is_used=False)

    @transaction_mode
    async def create_and_send_invite(self, email: str):
        """Create a new invite and send it to the provided email address.

        Args:
            email (str): The recipient's email address.

        Raises:
            HTTPException: If an active invite already exists for the email.

        """
        existing_invite = await self.get_unused_invite_by_email(email)
        if existing_invite:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="An active invite already exists for this email.",
            )
        invite = await self.create_invite(email)
        await self.send_invite(invite)

    @transaction_mode
    async def check_invite_token(self, token: str, email: str) -> bool:
        """Validate an invite token for a specific email and mark it as used if valid.

        Args:
            token (str): The invite token to validate.
            email (str): The email address associated with the token.

        Returns:
            bool: True if the token is valid, otherwise False.

        Raises:
            HTTPException: If the invite token is invalid or has already been used.

        """
        existing_invite: InviteModel = await self.repository.get_by_query_one_or_none(token=token, email=email, is_used=False)
        if existing_invite:
            existing_invite.is_used = True
            return True
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Invite is invalid")

    @transaction_mode
    async def create_invite(self, email) -> InviteModel:
        """Create a new invite for the specified email address.

        Args:
            email (str): The email address to associate with the invite.

        Returns:
            InviteModel: The created invite object.

        """
        invite_token = "".join(secrets.choice(string.digits) for _ in range(6))
        return await self.repository.add_one_and_get_object(token=invite_token, email=email)

    @staticmethod
    async def send_invite(invite: InviteModel):
        """Send an invite email to the recipient.

        Args:
            invite (InviteModel): The invite object containing the email and token.

        """
        email_body = f"Здравствуйте! Ваш токен: {invite.token}. Благодарим за использование нашего сервиса."
        send_email(invite.email, "Your token", email_body)
