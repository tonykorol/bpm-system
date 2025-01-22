from typing import TYPE_CHECKING

from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from src.schemas.user import UserSchema


class CompanyBaseSchema(BaseModel):
    name: str


class CompanyCreateSchema(CompanyBaseSchema):
    pass


class CompanySchema(CompanyBaseSchema):
    id: int


class CompanyWithUsersSchema(CompanySchema):
    users: list["UserSchema"] = Field(default_factory=list)
