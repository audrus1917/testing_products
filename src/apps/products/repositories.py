"""Репозиторий приложения ``products``."""


from src.database.alchemy.repositories import AlchemyRepository
from src.apps.products.models import Product


class ProductRepository(AlchemyRepository):
    """Класс репозитория для работы с товарами."""

    model = Product

