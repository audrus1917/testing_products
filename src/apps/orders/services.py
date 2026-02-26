from src.core.services.crud import AsyncCRUDService

from src.apps.orders.models import Order, OrderItem
from src.apps.orders.repositories import OrderRepository, OrderItemRepository
from src.database.alchemy.unit_of_work import AlchemyUnitOfWork
from src.core.database.repositories import AsyncRepository

class OrderService(AsyncCRUDService):
    repository = OrderRepository

    def __init__(
        self,
        uow: AlchemyUnitOfWork,
        repository: AsyncRepository,
    ):
        super().__init__(uow, repository)

        self.items_repository = OrderItemRepository(uow.session, OrderItem)