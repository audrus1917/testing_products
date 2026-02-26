from typing import Optional

from sqlalchemy import select

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

    async def add_item(
        self,
        model: Order,
        obj_data: dict
    ) -> Order:
        """Добавляет новый товар в заказ."""

        items, total = await self.items_repository.filter(
            query=select(OrderItem).where(
                OrderItem.order_id == model.id,
                OrderItem.product_id == obj_data["product_id"]
            ),
        )
        if total == 0:
            order_item = await self.items_repository.save(obj_data=obj_data)
        elif total == 1:
            order_item = items[0]
            order_item.amount += obj_data["amount"]

        await self.uow.session.flush()
        await self.uow.session.commit()

        updated_order_model = await self.get_by_id(model.id)
        return updated_order_model
