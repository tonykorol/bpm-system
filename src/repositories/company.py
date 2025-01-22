from src.models.company import CompanyModel
from src.utils.repository import SqlAlchemyRepository


class CompanyRepository(SqlAlchemyRepository):
    """Repository class for managing company data and user assignments to positions."""

    model = CompanyModel
