"""Репозиторий приложения ``Категории``."""

from src.database.alchemy.repositories import AlchemyRepository

from .models import Category


class CategoryRepository(AlchemyRepository):
    model = Category
