from src.models.user import UserModel
from src.utils.repository import SqlAlchemyRepository


class UserRepository(SqlAlchemyRepository):
    model = UserModel
