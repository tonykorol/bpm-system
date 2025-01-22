from pydantic import BaseModel

class PositionBaseSchema(BaseModel):
    name: str
    department_id: int


class PositionSchema(PositionBaseSchema):
    id: int


class PositionResponse(BaseModel):
    payload: PositionSchema


class PositionCreateRequest(PositionBaseSchema):
    pass


class PositionUpdateRequest(BaseModel):
    name: str


class PositionDeleteResponse(BaseModel):
    status: bool


class PositionAssignRequest(BaseModel):
    user_id: int
    position_id: int


class PositionAssignResponse(BaseModel):
    user_id: int
    position: PositionSchema
