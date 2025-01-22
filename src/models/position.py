from typing import TYPE_CHECKING, Any

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import BaseModel

if TYPE_CHECKING:
    from src.models import DepartmentModel, UserModel


class PositionModel(BaseModel):
    __tablename__ = "positions"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id"))

    department: Mapped["DepartmentModel"] = relationship(back_populates="positions")
    employees: Mapped[list["UserModel"]] = relationship(back_populates="position")

    def to_pydantic_schema(self) -> Any:
        from ..schemas.position import PositionSchema

        return PositionSchema(**self.__dict__)
