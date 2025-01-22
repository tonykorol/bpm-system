from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import BaseModel
from src.schemas.company import CompanySchema

if TYPE_CHECKING:
    from src.models import DepartmentModel, UserModel


class CompanyModel(BaseModel):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now())

    users: Mapped[list["UserModel"]] = relationship(back_populates="company")
    departments: Mapped[list["DepartmentModel"]] = relationship(back_populates="company")

    def to_pydantic_schema(self) -> CompanySchema:
        # Создайте словарь, исключая _sa_instance_state
        company_dict = {key: value for key, value in self.__dict__.items() if key != "_sa_instance_state"}
        return CompanySchema(**company_dict)
