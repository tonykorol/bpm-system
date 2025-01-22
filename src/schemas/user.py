from pydantic import BaseModel, EmailStr

from src.models.user import UserRole


class UserBaseSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    company_id: int
    role: UserRole
    department_id: int | None = None


class UserSchema(UserBaseSchema):
    id: int


class UserCreateSchema(UserBaseSchema):
    password: str


class UserCreateWithoutPasswordRequest(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr


class UserCreateWithoutPasswordResponse(BaseModel):
    payload: UserSchema


class UserSetPasswordRequest(BaseModel):
    email: EmailStr
    password: str


class UserSetPasswordResponse(BaseModel):
    payload: UserSchema


class GetMeResponse(UserSchema):
    role: str


class UserAuthSchema(UserSchema):
    password: str


class UserUpdateRequest(BaseModel):
    first_name: str
    last_name: str


class UserUpdateResponse(BaseModel):
    payload: UserSchema
