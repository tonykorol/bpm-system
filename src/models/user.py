from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Any

from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.position import UserPosition

from .base import BaseModel

if TYPE_CHECKING:
    from src.models import CompanyModel, DepartmentModel


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
    password: Mapped[str] = mapped_column(nullable=True, default=None)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now())

    positions: Mapped[list["UserPosition"]] = relationship(back_populates="user")

    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id"), nullable=True)
    department: Mapped["DepartmentModel"] = relationship(back_populates="employees", foreign_keys="UserModel.department_id")

    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id", ondelete="CASCADE"), nullable=True)
    company: Mapped["CompanyModel"] = relationship(back_populates="users")

    department_head: Mapped["DepartmentModel"] = relationship(back_populates="head", foreign_keys="DepartmentModel.head_id")

    def to_pydantic_schema(self) -> Any:
        from ..schemas.user import UserSchema

        return UserSchema(**self.__dict__)
