from fastapi import APIRouter, Depends
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from src.models import CompanyModel
from src.schemas.auth import (
    CheckAccountRequest,
    CheckAccountResponse,
    SignUpCompleteRequest,
    SignUpCompleteResponse,
    SignUpRequest,
    SignUpResponse,
)
from src.services.company import CompanyService
from src.services.invite import InviteService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.get(
    path="/check_account/{email}",
    status_code=HTTP_200_OK,
    response_model=CheckAccountResponse,
)
async def check_account(
        payload: CheckAccountRequest = Depends(CheckAccountRequest),
        service: CompanyService = Depends(CompanyService),
):
    email_is_free = await service.check_email(email=payload.email)
    return CheckAccountResponse(available=email_is_free)


@router.post(
    path="/sign-up",
    status_code=HTTP_200_OK,
    response_model=SignUpResponse,
)
async def sign_up(
        payload: SignUpRequest,
        invite_service: InviteService = Depends(InviteService),
):
    invite_is_valid = await invite_service.check_invite_token(payload.token, payload.account)
    return SignUpResponse(success=invite_is_valid)


@router.post(
    path="/sign-up-complete",
    status_code=HTTP_201_CREATED,
)
async def sign_up_complete(
        payload: SignUpCompleteRequest,
        company_service: CompanyService = Depends(CompanyService),
):
    created_company: CompanyModel = await company_service.create_company_and_user(payload)
    return SignUpCompleteResponse(
        company=created_company.to_pydantic_schema(),
    )
