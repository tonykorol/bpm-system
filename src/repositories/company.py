from src.models.company import CompanyModel
from src.utils.repository import SqlAlchemyRepository


class CompanyRepository(SqlAlchemyRepository):
    model = CompanyModel
