from fastapi import APIRouter, Depends, HTTPException, Query
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK

from src.models import DepartmentModel
from src.schemas.department import DepartmentCreateRequest, DepartmentCreateResponse, DepartmentGetResponse
from src.services.auth import get_current_user
from src.services.department import DepartmentService

router = APIRouter(prefix="/department", tags=["department"])


@router.post(
    path='/',
    status_code=HTTP_201_CREATED,
    response_model=DepartmentCreateResponse
)
async def create_department(
        department_data: DepartmentCreateRequest,
        current_user: dict = Depends(get_current_user),
        service: DepartmentService = Depends(DepartmentService),
):
    department: DepartmentModel = await service.create_department(department_data=department_data, current_user=current_user)
    return DepartmentCreateResponse(payload=department.to_pydantic_schema())


@router.get(
    path='/{id}',
    status_code=HTTP_200_OK,
    response_model=DepartmentGetResponse,
)
async def get_department_info(
        dep_id: int = Query(gt=0),
        # current_user: dict = Depends(get_current_user),
        service: DepartmentService = Depends(DepartmentService),
):
    department: DepartmentModel = await service.get_department_by_id(department_id=dep_id)
    return DepartmentGetResponse(department=department.to_pydantic_schema())


# @router.get(
#     path='/tree',
#     status_code=HTTP_200_OK,
#     # response_model=
# )
# async def get_department_tree(
#
# )
