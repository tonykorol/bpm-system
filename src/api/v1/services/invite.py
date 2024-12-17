import secrets

from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

from src.api.v1.services.utils.email_sender import send_email
from src.models.invite import InviteModel
from src.utils.service import BaseService
from src.utils.unit_of_work import transaction_mode


class InviteService(BaseService):
    base_repository = "invite"

    @transaction_mode
    async def get_unused_invite_by_email(self, email: str) -> InviteModel:
        return await self.uow.invite.get_by_query_one_or_none(email=email, is_used=False)

    @transaction_mode
    async def create_and_send_invite(self, email: str):
        existing_invite = await self.get_unused_invite_by_email(email)
        if existing_invite:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="An active invite already exists for this email."
            )
        invite = await self.create_and_get_invite(email)
        await self.send_invite(email, invite)

    @transaction_mode
    async def check_invite_token(self, token: str, email: str) -> bool:
        existing_invite: InviteModel = await self.uow.invite.get_by_query_one_or_none(token=token, email=email, is_used=False)
        if existing_invite:
            existing_invite.is_used = True
            return True
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Invite is invalid")

    @transaction_mode
    async def create_and_get_invite(self, email) -> InviteModel:
        invite_token = ''.join(secrets.choice('0123456789') for _ in range(6))
        return await self.uow.invite.add_one_and_get_object(token=invite_token, email=email)

    @staticmethod
    async def send_invite(email: str, invite: InviteModel):
        email_body = f"For complete registration enter this token {invite.token}"
        send_email(email, "Your token", email_body)

