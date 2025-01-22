from pydantic import BaseModel


class PositionBaseSchema(BaseModel):
    name: str

class PositionSchema(PositionBaseSchema):
    id: int
    department_id: int


class PositionCreateRequest(PositionBaseSchema):
    pass


class PositionCreateResponse(BaseModel):
    position: PositionSchema


class PositionAssignRequest(BaseModel):
    position_id: int
    user_id: int
