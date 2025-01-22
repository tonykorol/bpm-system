from fastapi import APIRouter, Depends
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from src.models import PositionModel
from src.schemas.auth import TokenPayload
from src.schemas.position import (
    PositionAssignRequest,
    PositionAssignResponse,
    PositionCreateRequest,
    PositionDeleteResponse,
    PositionResponse,
    PositionUpdateRequest,
)
from src.services.auth import get_current_user
from src.services.position import PositionService

router = APIRouter(prefix="/position", tags=["Positions"])


@router.post(
    path="/",
    status_code=HTTP_201_CREATED,
    response_model=PositionResponse,
)
async def create_position(
        position_data: PositionCreateRequest,
        current_user: TokenPayload = Depends(get_current_user),
        service: PositionService = Depends(PositionService),
):
    position: PositionModel = await service.create_position(position_data)
    return PositionResponse(payload=position.to_pydantic_schema())


@router.get(
    path="/{pos_id}",
    status_code=HTTP_200_OK,
    response_model=PositionResponse,
)
async def get_position(
        pos_id: int,
        current_user: TokenPayload = Depends(get_current_user),
        service: PositionService = Depends(PositionService),
):
    position: PositionModel = await service.get_position_by_id(pos_id)
    return PositionResponse(payload=position.to_pydantic_schema())


@router.patch(
    path="/{pos_id}",
    status_code=HTTP_200_OK,
    response_model=PositionResponse,
)
async def update_position(
        pos_id: int,
        position_data: PositionUpdateRequest,
        current_user: TokenPayload = Depends(get_current_user),
        service: PositionService = Depends(PositionService),
):
    updated_position: PositionModel = await service.update_position(pos_id, position_data)
    return PositionResponse(payload=updated_position.to_pydantic_schema())


@router.delete(
    path="/{pos_id}",
    status_code=HTTP_200_OK,
    response_model=PositionDeleteResponse,
)
async def delete_position(
        pos_id: int,
        current_user: TokenPayload = Depends(get_current_user),
        service: PositionService = Depends(PositionService),
):
    status = await service.delete_position(pos_id)
    return PositionDeleteResponse(status=status)


@router.post(
    path="/assign",
    status_code=HTTP_200_OK,
    response_model=PositionAssignResponse,
)
async def assign_user_to_position(
        payload: PositionAssignRequest,
        current_user: TokenPayload = Depends(get_current_user),
        service: PositionService = Depends(PositionService),
):
    position: PositionModel = await service.assign_user_to_position(payload)
    return PositionAssignResponse(
        user_id=payload.user_id,
        position=position.to_pydantic_schema(),
    )
