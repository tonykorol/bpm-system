from typing import TYPE_CHECKING, Any

from sqlalchemy import String, ForeignKey, Integer
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
    users_positions: Mapped[list["UserPosition"]] = relationship(back_populates="position")

    def to_pydantic_schema(self) -> Any:
        from ..schemas.position import PositionSchema

        return PositionSchema(**self.__dict__)


class UserPosition(BaseModel):
    __tablename__ = "users_positions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    position_id: Mapped[int] = mapped_column(ForeignKey("positions.id"))

    user: Mapped["UserModel"] = relationship(back_populates="positions")
    position: Mapped["PositionModel"] = relationship(back_populates="users_positions")

