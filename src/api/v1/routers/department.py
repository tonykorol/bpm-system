from fastapi import APIRouter, Depends
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from src.models import DepartmentModel
from src.schemas.auth import TokenPayload
from src.schemas.department import (
    DepartmentCreateRequest,
    DepartmentDeleteResponse,
    DepartmentResponse,
    DepartmentSetHeadRequest,
    DepartmentUpdateRequest,
)
from src.services.auth import get_current_user
from src.services.department import DepartmentService

router = APIRouter(prefix="/department", tags=["department"])


@router.post(
    path="/",
    status_code=HTTP_201_CREATED,
    response_model=DepartmentResponse,
)
async def create_department(
        department: DepartmentCreateRequest,
        current_user: TokenPayload = Depends(get_current_user),
        service: DepartmentService = Depends(DepartmentService),
):
    department: DepartmentModel = await service.create_department(department)
    return DepartmentResponse(payload=department.to_pydantic_schema())


@router.get(
    path="/{dep_id}",
    status_code=HTTP_200_OK,
    response_model=DepartmentResponse,
)
async def get_department(
        dep_id: int,
        current_user: TokenPayload = Depends(get_current_user),
        service: DepartmentService = Depends(DepartmentService),
):
    department: DepartmentModel = await service.get_department_by_id(dep_id)
    return DepartmentResponse(payload=department.to_pydantic_schema())


@router.patch(
    path="/{dep_id}",
    status_code=HTTP_200_OK,
    response_model=DepartmentResponse,
)
async def update_department(
        dep_id: int,
        department_data: DepartmentUpdateRequest,
        current_user: TokenPayload = Depends(get_current_user),
        service: DepartmentService = Depends(DepartmentService),
):
    updated_department: DepartmentModel = await service.update_department(dep_id, department_data)
    return DepartmentResponse(payload=updated_department.to_pydantic_schema())


@router.delete(
    path="/{dep_id}",
    status_code=HTTP_200_OK,
    response_model=DepartmentDeleteResponse,
)
async def delete_department(
        dep_id: int,
        current_user: TokenPayload = Depends(get_current_user),
        service: DepartmentService = Depends(DepartmentService),
):
    res: bool = await service.delete_department(dep_id)
    return DepartmentDeleteResponse(status=res)


@router.post(
    path="/set_head",
    status_code=HTTP_200_OK,
    response_model=DepartmentResponse,
)
async def set_department_head(
        payload: DepartmentSetHeadRequest,
        current_user: TokenPayload = Depends(get_current_user),
        service: DepartmentService = Depends(DepartmentService),
):
    department: DepartmentModel = await service.set_department_head(payload)
    return DepartmentResponse(payload=department.to_pydantic_schema())
