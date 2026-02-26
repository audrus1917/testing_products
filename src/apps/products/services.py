from src.core.services.crud import AsyncCRUDService

from src.apps.products.models import Product
from src.apps.products.repositories import ProductRepository


class ProductService(AsyncCRUDService):
    repository = ProductRepository