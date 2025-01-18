from src.models import DepartmentModel
from src.utils.repository import SqlAlchemyRepository


class DepartmentRepository(SqlAlchemyRepository):
    model = DepartmentModel