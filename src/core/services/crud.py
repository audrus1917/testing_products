"""Класс сервиса для `CRUD`."""

from typing import Type, TypeVar, Union, Optional, Dict, Any, Collection

from src.core.database.repositories import AsyncRepository
from src.core.database.unit_of_work import AsyncUnitOfWork
from src.core.services.base import AsyncService


ModelT = TypeVar("ModelT")
QueryT = TypeVar("QueryT")


class AsyncCRUDService[ModelT](AsyncService):
    def __init__(
        self,
        uow: AsyncUnitOfWork,
        repository: AsyncRepository
    ):
        self.uow = uow
        self.repository = repository

    async def get(
        self,
        query: Optional[QueryT] = None,
    ) -> ModelT:
        return await self.repository.get(query=query)

    async def filter(
        self,
        query: Optional[QueryT] = None,
    ) -> Collection[ModelT]:
        """Возвращает коллекцию моделей, выбранных по запросу."""
        return await self.repository.filter(query=query)

    async def create(self, obj_data: Union[dict, ModelT]) -> ModelT:
        """Создает и возвращает модель."""
        async with self.uow:
            if isinstance(obj_data, dict):
                obj = await self.repository.save(obj_data=obj_data)
            else:
                obj = await self.repository.save(obj=obj_data)

            await self.uow.commit()

        await self.repository.refresh(obj)
        return obj

    async def update(
        self,
        obj: Optional[ModelT] = None,
        query: Optional[QueryT] = None,
        update_values: Optional[Dict[Any, Any]] = None,
    ) -> None:
        """Обновляет выбранную модель или по заданному запросу :cls:`Select."""

        async with self.uow:
            await self.repository.update(
                obj=obj, query=query, update_values=update_values
            )
            await self.uow.commit()

    async def delete(self, *filters, **kwargs_filters) -> None:
        async with self.uow:
            obj = await self.get(*filters, **kwargs_filters)
            await self.repository.delete(obj)
            await self.uow.commit()

    def __repr__(self):
        return f"CRUD service[{self.repository.model.__name__}]"


__all__ = [
    "AsyncCRUDService",
]
