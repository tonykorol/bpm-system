from pydantic import BaseModel, EmailStr, Field

from src.schemas.company import CompanySchema


class CheckAccountResponse(BaseModel):
    available: bool


class CheckAccountRequest(BaseModel):
    email: EmailStr


class SignUpRequest(BaseModel):
    account: EmailStr
    token: str


class SignUpResponse(BaseModel):
    success: bool


class SignUpCompleteRequest(BaseModel):
    account: EmailStr
    password: str
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="First name must be between 1 and 50 characters."
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Last name must be between 1 and 50 characters."
    )
    company_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Company name must be between 1 and 50 characters."
    )


class SignUpCompleteResponse(BaseModel):
    company: CompanySchema


class AccessTokenScema(BaseModel):
    token: str
    token_type: str


class TokenPayload(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    company_id: int
    role: str
    department_id: int | None
