import re
from typing import Optional

from pydantic import BaseModel, field_validator, Field
from sqlalchemy_utils import Ltree


class DepartmentBaseSchema(BaseModel):
    name: str
    parent_department_id: Optional[int] = None
    company_id: int

    @field_validator('name')
    def validate_name(cls, value: str) -> str:
        if re.search(r'[^\w\s]', value):
            raise ValueError("There should be no punctuation marks in the department name.")
        return value


class DepartmentSchema(DepartmentBaseSchema):
    id: int
    path: str
    head_id: Optional[int] = None

    @field_validator("path", mode="before")
    def convert_ltree_to_string(cls, value):
        if isinstance(value, Ltree):
            return str(value)  # Преобразуем Ltree в строку
        return value


class DepartmentResponse(BaseModel):
    payload: DepartmentSchema


class DepartmentCreateRequest(DepartmentBaseSchema):
    pass


class DepartmentUpdateRequest(BaseModel):
    name: str


class DepartmentDeleteResponse(BaseModel):
    status: bool


class DepartmentSetHeadRequest(BaseModel):
    user_id: int
    department_id: int
