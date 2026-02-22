from src.core.services.crud import AsyncCRUDService

from src.apps.categories.models import Category


class CategoryService[Category](AsyncCRUDService):
    pass
