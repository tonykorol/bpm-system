from fastapi import APIRouter, Depends
from starlette.status import HTTP_200_OK

from src.models import PositionModel
from src.schemas.auth import TokenPayload
from src.schemas.position import PositionCreateRequest, PositionCreateResponse
from src.services.auth import get_current_user
from src.services.position import PositionService

router = APIRouter(prefix='/position', tags=['Positions'])


@router.post(
    path='/',
    status_code=HTTP_200_OK,
    response_model=PositionCreateResponse
)
async def create_position(
        position_data: PositionCreateRequest,
        current_user: TokenPayload = Depends(get_current_user),
        service: PositionService = Depends(PositionService)
):
    position: PositionModel = await service.create_position(current_user, position_data)
    return PositionCreateResponse(position=position.to_pydantic_schema())


# @router.post(
#     path='/{position_id}/assign',
#     status_code=HTTP_200_OK,
#     # response_model=
# )
# async def assign_position(
#         assignee: PositionAssignRequest,
#         # current_user: TokenPayload = Depends(get_current_user),
#         service: PositionService = Depends(PositionService)
# ):
#     return await service.assign_user_to_position(user_id=assignee.user_id, position_id=assignee.position_id)
