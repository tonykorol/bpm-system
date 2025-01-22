from src.models.user import UserModel
from src.utils.repository import SqlAlchemyRepository


class UserRepository(SqlAlchemyRepository):
    """Repository class for managing user data and user assignments to positions."""

    model = UserModel
