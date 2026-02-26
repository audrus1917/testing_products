"""Репозиторий приложения ``Пользователи``."""

from src.database.alchemy.repositories import AlchemyRepository
from src.apps.users.models import User

class UserRepository(AlchemyRepository):
    model = User
