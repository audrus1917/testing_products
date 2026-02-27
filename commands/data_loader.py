#!/usr/bin/env python3

"""Скрипт заполнения БД тестовыми данными для задач."""

from __future__ import annotations
from typing import Optional, Any

import uuid
import string
import random
import asyncio
import json
import logging
import pendulum

from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

import faker

from src.database.alchemy import engine

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

from src.apps.orders.enums import OrderStatus

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

    def load_data(self, data_file: Path) -> Optional[dict[str, Any]]:
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

        _, total = await self.category_repo.filter()
        logger.debug(f"Найдено категорий: {total}")
        if total == 0:
            data = self.load_data(DATA_FOLDER / "categories.json")
            if data:
                await _walk(data)

    async def load_manufacturers(self):
        """Загрузка тестовых производителей в БД."""

        _, total = await self.manufacturer_repo.filter()
        logger.debug(f"Найдено производителей: {total}")
        if total == 0:
            data = self.load_data(DATA_FOLDER / "manufacturers.json")
            if data:
                for item in data.get("items", []):
                    del item["type"]
                    del item["country"]
                    await self.manufacturer_repo.save(obj_data=item)

    async def load_products(self):
        """Загрузка тестовых продуктов в БД."""

        _, total = await self.product_repo.filter()
        if total > 0:
            logger.debug(f"Найдено продуктов: {total}")
            return
        
        # Категории без "дочерних" (листья)
        leaves = await self.category_repo.get_leaves()
        if not leaves:
            logger.warning(
                "Нет категорий для загрузки продуктов. "
                "Сначала загрузите категории."
            )
            return

        manufacturers, total = await self.manufacturer_repo.filter()
        logger.debug(f"Найдено производителей: {total}")
        if not manufacturers:
            logger.warning(
                "Нет производителей для загрузки продуктов. "
                "Сначала загрузите производителей."
            )
            return
        
        manufacturer_ids = [manufacturer.id for manufacturer in manufacturers]

        for category in leaves:
            for idx in range(random.randint(1, 5)):
                product_name = (
                        f"{category.name}, модель "
                        f"{random.choice(string.ascii_uppercase)}-{idx}"
                    )
                item = {
                    "name": product_name,
                    "description": f"Описание продукта для {product_name}",
                    "price": random.randint(2000, 20000),
                    "category_id": category.id,
                    "manufacturer_id": random.choice(manufacturer_ids)
                }
                added_product = await self.product_repo.save(obj_data=item)
                logger.debug(f"Добавлен продукт: {added_product}")

    async def load_clients(self):
        """Загрузка тестовых клиентов в БД."""

        fake = faker.Faker("ru_RU")

        _, total = await self.client_repo.filter()
        logger.debug(f"Найдено клиентов: {total}")
        if total == 0:
            for idx in range(1, 11):
                item = {
                    "last_name": fake.last_name_male(),
                    "first_name": fake.first_name_male(),
                    "phone": fake.phone_number(),
                    "address": fake.address(),
                    "balance": round(random.uniform(500, 10000), 2)
                }
                await self.client_repo.save(obj_data=item)

    async def load_orders(self):
        """Загрузка тестовых заказов в БД."""

        _, total = await self.order_repo.filter()
        logger.debug(f"Найдено заказов: {total}")
        if total > 0:
            return

        clients, clients_total = await self.client_repo.filter()
        logger.debug(f"Найдено клиентов: {total}")
        if not clients:
            logger.warning(
                "Нет клиентов для загрузки заказов. "
                "Сначала загрузите клиентов."
            )
            return

        products, total = await self.product_repo.filter()
        logger.debug(f"Найдено продуктов: {total}")
        if not products:
            logger.warning(
                "Нет продуктов для загрузки заказов. "
                "Сначала загрузите продукты."
            )
            return

        for client in clients:
            for order_idx in range(random.randint(1, 6)):
                registration_date = pendulum.now().subtract(days=random.randint(1, 90))
                payment_date = registration_date.add(days=random.randint(1, 4))
                order_data = {
                    "order_no": uuid.uuid4().hex[:8].upper(),
                    "client_id": client.id,
                    "status": OrderStatus.PAID,
                    "registration_date": registration_date,
                    "payment_date": payment_date,

                }
                order = await self.order_repo.save(obj_data=order_data)

                for _ in range(random.randint(1, 5)):
                    product = random.choice(products)
                    order_item_data = {
                        "order_id": order.id,
                        "product_id": product.id,
                        "price": product.price,
                        "amount": random.randint(1, 3)
                    }
                    await self.order_item_repo.save(obj_data=order_item_data) 


async def main():

    # Получение асинхронной сессии
    AsyncSessionLocal = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
    )

    async with AsyncSessionLocal() as session:
        loader = Loader(session)

        # Запуск загрузки данных
        await loader.load_categories()
        await loader.load_manufacturers()
        await loader.load_products()
        await loader.load_clients()
        await loader.load_orders()
        await session.commit()


if __name__ == "__main__":

    # Запуск загрузки данных
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())