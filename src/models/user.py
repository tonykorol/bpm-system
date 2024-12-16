from datetime import datetime

from base import BaseModel
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.company import CompanyModel


class UserModel(BaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(256), unique=True)
    hashed_password: Mapped[str]
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]

    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id", ondelete="CASCADE"))
    company: Mapped[CompanyModel] = relationship(back_populates="users")
