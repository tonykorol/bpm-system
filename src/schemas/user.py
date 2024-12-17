from pydantic import BaseModel, EmailStr

from src.models.user import UserRole


class UserBaseSchema(BaseModel):

    first_name: str
    last_name: str
    email: EmailStr
    role: "UserRole"


class UserCreateSchema(UserBaseSchema):
    password: str


class UserUpdateSchema(UserBaseSchema):
    pass


class UserSchema(UserBaseSchema):
    id: int
    company_id: int
