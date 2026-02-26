"""Репозиторий приложения ``orders``."""


from src.database.alchemy.repositories import AlchemyRepository
from src.apps.orders.models import Order, OrderItem


class OrderRepository(AlchemyRepository):
    """Класс репозитория для работы с заказами."""

    model = Order


class OrderItemRepository(AlchemyRepository):
    """Класс репозитория для работы с позициями заказов."""

    model = OrderItem
