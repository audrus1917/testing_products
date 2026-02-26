"""Базовый класс репозитория для ``SQLAlchemy``."""

from typing import Type, Optional, TypeVar, Collection, Dict, Any, Tuple

from sqlalchemy import select, update, delete, func
from sqlalchemy.sql.selectable import Select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.utils import update_model_from_dict
from src.core.error_wrapper import ErrorWrapper
from src.core.database.exceptions import InvalidQueryError, NotFoundError
from src.database.alchemy import Base
from src.database.alchemy.error_wrapper import AlchemyErrorWrapper
from src.database.alchemy.model_utils import dict_to_alchemy_models

AlchemyModelT = TypeVar('AlchemyModelT', bound=Base)


class AlchemyRepository[AlchemyModelT]:
    session: AsyncSession
    model: Type[AlchemyModelT]

    def __init__(
        self,
        session: AsyncSession,
        model: Type[AlchemyModelT],
        initial_query: Optional[Select] = None,
        error_wrapper: Optional[ErrorWrapper] = None,
    ):
        self.session = session
        self.model = model
        # Базовый запрос
        self.__initial_query: Optional[Select] = (
            initial_query if initial_query is not None else select(model)
        )
        self.error_wrapper = error_wrapper or AlchemyErrorWrapper()
        self.get = self.error_wrapper.decorate(self.get)
        self.filter = self.error_wrapper.decorate(self.filter)
        self.save = self.error_wrapper.decorate(self.save)
        self.delete = self.error_wrapper.decorate(self.delete)
        self.update = self.error_wrapper.decorate(self.update)
        self.refresh = self.error_wrapper.decorate(self.refresh)

    def get_initial_query(self, override_query: Optional[Select] = None) -> Select:
        if override_query is not None:
            return override_query
        
        if self.__initial_query is not None:
            return self.__initial_query
        else:
            raise AssertionError(
                "You must either pass the initial "
                "query or define ``get_initial_query()``"
            )

    def to_model(self, data: Dict[Any, Any]) -> AlchemyModelT:
        return self.model(**dict_to_alchemy_models(data=data, model=self.model))

    async def get(
        self,
        query: Optional[Select] = None,
    ) -> Optional[AlchemyModelT]:
        overriden_query: Select = self.get_initial_query(query)
        if overriden_query.whereclause is None:
            raise InvalidQueryError
        res = await self.session.execute(overriden_query)
        result = res.one_or_none()
        return result[0] if result is not None else None

    async def get_by_id(
        self,
        id_value: Any
    ) -> AlchemyModelT:
        overriden_query: Select = self.get_initial_query().where(self.model.id == id_value)
        if overriden_query.whereclause is None:
            raise InvalidQueryError
        res = await self.session.execute(overriden_query)
        result = res.one_or_none()
        if result is None:
            raise NotFoundError(f"Model {self.model.__name__} with id {id_value} not found")    
        
        return result[0]


    async def filter(
        self,
        query: Optional[Select] = None,
        **kwargs,
    ) -> Tuple[Collection[AlchemyModelT], int]:
        overriden_query = self.get_initial_query(query)
        query_filters = kwargs.pop("query_filters", None)
        overriden_query = query_filters.filter(overriden_query) \
            if query_filters else overriden_query

        count_query =  select(func.count()).select_from(overriden_query.subquery())
        count_result = await self.session.execute(count_query)
        total = count_result.scalar_one()
        
        result = await self.session.execute(overriden_query)
        return (result.scalars().all(), total)

    async def save(
        self,
        obj: Optional[AlchemyModelT] = None,
        obj_data: Optional[Dict[Any, Any]] = None,
    ) -> Optional[AlchemyModelT]:

        if obj is None and obj_data is not None:
            obj = self.to_model(obj_data)

        self.session.add(obj)
        await self.session.flush()
        return obj

    async def update(
        self,
        model: AlchemyModelT,
        update_values: Dict[Any, Any],
    ) -> AlchemyModelT:
        update_model_from_dict(model, update_values)
        if model is not None and model not in self.session:
            model = await self.session.merge(model)
            self.session.add(model)
        await self.session.flush([model,])
        return model

    async def update_many(
        self,
        query: Select,
        update_values: Dict[Any, Any],
    ) -> None:
        if isinstance(query, Select) and update_values:
            stmt = update(self.model)
            if query.whereclause is not None:
                stmt = stmt.where(query.whereclause)

            await self.session.execute(
                stmt.values(update_values).execution_options(synchronize_session=False)
            )

    async def delete(
        self,
        model: AlchemyModelT
    ) -> None:
        if model is not None:
            await self.session.delete(model)

    async def delete_many(
        self,
        query: Select
    ) -> None:
        if isinstance(query, Select):
            stmt = delete(self.model)
            if query.whereclause is not None:
                stmt = stmt.where(query.whereclause)
            await self.session.execute(
                stmt.execution_options(synchronize_session=False)
            )

    async def refresh(self, obj: AlchemyModelT) -> None:
        if obj not in self.session:
            obj = await self.session.merge(obj)

        await self.session.refresh(obj)

    def is_modified(self, obj: AlchemyModelT) -> bool:
        return obj in self.session and self.session.is_modified(obj)


__all__ = [
    'AlchemyRepository',
]
