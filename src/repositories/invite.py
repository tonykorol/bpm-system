from src.models.invite import InviteModel
from src.utils.repository import SqlAlchemyRepository


class InviteRepository(SqlAlchemyRepository):
    model = InviteModel

    @staticmethod
    async def mark_as_used(invite: InviteModel):
        invite.is_used = True
