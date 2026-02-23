"""Репозиторий приложения ``Пользователи``."""

from src.database.alchemy.repositories import AlchemyRepository
from src.apps.categories.models import Category


class CategoryRepository(AlchemyRepository):
    model = Category
