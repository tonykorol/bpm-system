from src.models import PositionModel
from src.utils.repository import SqlAlchemyRepository


class PositionRepository(SqlAlchemyRepository):
    model = PositionModel