from typing import TYPE_CHECKING, Any

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import Ltree, LtreeType

from src.models import BaseModel

if TYPE_CHECKING:
    from src.models import PositionModel, CompanyModel, UserModel


class DepartmentModel(BaseModel):
    __tablename__ = 'departments'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    path: Mapped[Ltree] = mapped_column(LtreeType)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"))
    head_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    positions: Mapped[list["PositionModel"]] = relationship(back_populates="department")
    employees: Mapped[list["UserModel"]] = relationship(back_populates="department", foreign_keys="UserModel.department_id")
    company: Mapped["CompanyModel"] = relationship(back_populates="departments")
    head: Mapped["UserModel"] = relationship(back_populates="department_head", foreign_keys="DepartmentModel.head_id" )

    def to_pydantic_schema(self) -> Any:
        from ..schemas.department import DepartmentSchema

        return DepartmentSchema(**self.__dict__)
