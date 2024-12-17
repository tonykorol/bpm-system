from fastapi import APIRouter, Depends
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from src.api.v1.services.company import CompanyService
from src.api.v1.services.invite import InviteService
from src.api.v1.services.user import UserService
from src.models import CompanyModel, UserModel
from src.models.user import UserRole
from src.schemas.auth import CheckAccountResponse, CheckAccountRequest, SignUpRequest, SignUpResponse, \
    SignUpCompleteRequest, SignUpCompleteResponse
from src.schemas.company import CompanyCreateSchema
from src.schemas.user import UserCreateSchema

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.get(
    path="/check_account/{email}",
    status_code=HTTP_200_OK,
    response_model=CheckAccountResponse
)
async def check_account(
        payload: CheckAccountRequest = Depends(CheckAccountRequest),
        user_service: UserService = Depends(UserService),
        invite_service: InviteService = Depends(InviteService)
):
    email = payload.email
    user = await user_service.get_user_by_email(email)
    if user is None:
        await invite_service.create_and_send_invite(email)
    return CheckAccountResponse(available=user is None)

@router.post(
    path="/sign-up",
    status_code=HTTP_200_OK,
    response_model=SignUpResponse
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
        user_service: UserService = Depends(UserService),
        company_service: CompanyService = Depends(CompanyService),
):
    company = CompanyCreateSchema(
        name=payload.company_name
    )
    user = UserCreateSchema(
        first_name=payload.first_name,
        last_name=payload.last_name,
        email=payload.account,
        password=payload.password,
        role=UserRole.COMPANY_ADMIN
    )

    created_company: CompanyModel = await company_service.create_company(company)
    created_user: UserModel = await user_service.create_user(user, company_id=created_company.id)
    return SignUpCompleteResponse(
        user=created_user.to_pydantic_schema(),
        company=created_company.to_pydantic_schema(),
    )
