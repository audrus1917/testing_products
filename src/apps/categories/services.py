from src.core.services.crud import AsyncCRUDService

from src.apps.categories.models import Category
from src.apps.categories.repositories import CategoryRepository


class CategoryService[Category](AsyncCRUDService):
    repository = CategoryRepository

