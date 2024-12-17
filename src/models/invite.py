from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import BaseModel


class InviteModel(BaseModel):
    __tablename__ = "invites"

    id: Mapped[int] = mapped_column(primary_key=True)
    token: Mapped[str] = mapped_column(unique=True)
    is_used: Mapped[bool] = mapped_column(default=False)
    email: Mapped[str]
