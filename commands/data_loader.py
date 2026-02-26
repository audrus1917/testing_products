#!/usr/bin/env python3

"""Скрипт заполнения БД тестовыми данными для задач."""

from __future__ import annotations
from typing import Optional, Union, Any

import asyncio
import json
import logging

from pathlib import Path

from src.database.alchemy import get_session

from src.apps.users.models import User
from src.apps.categories.models import Category
from src.apps.clients.models import Client
from src.apps.manufacturers.models import Manufacturer
from src.apps.products.models import Product
from src.apps.orders.models import Order, OrderItem

from src.apps.categories.repositories import CategoryRepository
from src.apps.clients.repositories import ClientRepository
from src.apps.manufacturers.repositories import ManufacturerRepository
from src.apps.products.repositories import ProductRepository
from src.apps.orders.repositories import OrderRepository, OrderItemRepository

DATA_FOLDER = Path(__file__).parent / "data"

logging.basicConfig(
    level=logging.DEBUG, 
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class Loader:
    """Класс для загрузки тестовых данных в БД"""

    def __init__(
        self,
        session: Any,
    ):
        # Инициализация репозиториев
        self.session = session
        self.category_repo = CategoryRepository(session, model=Category)
        self.manufacturer_repo = ManufacturerRepository(session, model=Manufacturer)
        self.product_repo = ProductRepository(session, model=Product)
        self.client_repo = ClientRepository(session, model=Client)
        self.order_repo = OrderRepository(session, model=Order)
        self.order_item_repo = OrderItemRepository(session, model=OrderItem)

    def load_data(self, data_file: Path) -> Optional[Union[dict, list]]:
        """Загрузка данных из JSON файла"""
        try:
            with open(data_file, "r", encoding="utf-8") as file:
                data = json.load(file)
                logger.debug(f"Данные успешно загружены из {data_file}")
                return data
        except FileNotFoundError:
            logger.error(f"Файл {data_file} не найден")
        except json.JSONDecodeError:
            logger.error(f"Ошибка декодирования JSON в файле {data_file}")
        return None

    async def load_categories(self):
        """Загрузка тестовых категорий в БД."""

        async def _walk(data: dict) -> Any:
            """Рекурсивная функция для обхода дерева категорий."""
            async def _walk_node(node: dict, parent_id: Optional[int] = None) -> None:

                node_data = {
                    "name": node["name"],
                    "parent_id": parent_id
                }
                model = await self.category_repo.save(obj_data=node_data)
                for child in node.get("children", []):
                    await _walk_node(child, parent_id=model.id)

            return await _walk_node(data)
        
        data = self.load_data(DATA_FOLDER / "categories.json")
        if data:
            await _walk(data)

    async def load_manufacturers(self):
        """Загрузка тестовых производителей в БД."""

async def main():

    # Получение асинхронной сессии
    session = await get_session().__anext__()
    import pdb; pdb.set_trace()
    loader = Loader(session)

    # Запуск загрузки данных
    await loader.load_categories()
    await loader.load_manufacturers()

    await session.commit()
    await session.close()


if __name__ == "__main__":

    # Запуск загрузки данных
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())