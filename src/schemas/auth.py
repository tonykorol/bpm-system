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
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    company_name: str = Field(..., min_length=1, max_length=50)


class SignUpCompleteResponse(BaseModel):
    company: CompanySchema


class AccessTokenScema(BaseModel):
    token: str
    token_type: str
