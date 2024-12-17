from datetime import datetime
from enum import Enum
from typing import Any

from .base import BaseModel
from sqlalchemy import ForeignKey, String, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.company import CompanyModel


class UserRole(Enum):
    ADMIN = "admin"
    COMPANY_ADMIN = "company_admin"
    USER = "user"


class UserModel(BaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(256), unique=True)
    role: Mapped[UserRole] = mapped_column(SQLEnum(UserRole), default=UserRole.USER)
    password: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now())

    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id", ondelete="CASCADE"), nullable=True)
    company: Mapped[CompanyModel] = relationship(back_populates="users")

    def to_pydantic_schema(self) -> Any:
        from ..schemas.user import UserSchema

        return UserSchema(**self.__dict__)
