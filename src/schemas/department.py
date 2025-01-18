import re
from typing import Optional

from pydantic import BaseModel, field_validator
from sqlalchemy_utils import Ltree


class DepartmentBaseSchema(BaseModel):
    name: str
    head_id: Optional[int] = None

    @field_validator('name')
    def validate_name(cls, value: str) -> str:
        if re.search(r'[\s\W]', value):
            raise ValueError("There should be no spaces or punctuation marks in the department name.")
        return value


class DepartmentSchema(DepartmentBaseSchema):
    id: int
    company_id: int
    path: str

    @field_validator("path", mode="before")
    def convert_ltree_to_string(cls, value):
        if isinstance(value, Ltree):
            return str(value)  # Преобразуем Ltree в строку
        return value


class DepartmentCreateRequest(DepartmentBaseSchema):
    pass


class DepartmentCreateResponse(BaseModel):
    payload: DepartmentSchema


class DepartmentGetResponse(BaseModel):
    department: DepartmentSchema
