"""Абстрактный класс для репозиториев."""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import (
    TypeVar,
    Generic,
    Optional,
    Type,
    Dict,
    Collection,
    Any,
)

from src.core.error_wrapper import ErrorWrapper


QueryT = TypeVar("QueryT")
ModelT = TypeVar("ModelT")
SessionT = TypeVar("SessionT")
AsyncSessionT = TypeVar("AsyncSessionT")


class Repository(Generic[SessionT, ModelT, QueryT], ABC):
    """Абстрактный класс для репозитория."""

    def __init__(
        self,
        session: SessionT,
        model: Type[ModelT],
        initial_query: Optional[QueryT] = None,
        error_wrapper: Optional[ErrorWrapper] = None,
    ):
        self.session = session
        self.model = model
        self.__initial_query: Optional[QueryT] = initial_query
        self.error_wrapper = error_wrapper or ErrorWrapper()
        self.get = self.error_wrapper.decorate(self.get)
        self.filter = self.error_wrapper.decorate(self.filter)
        self.save = self.error_wrapper.decorate(self.save)
        self.delete = self.error_wrapper.decorate(self.delete)
        self.update = self.error_wrapper.decorate(self.update)
        self.is_modified = self.error_wrapper.decorate(self.is_modified)
        self.refresh = self.error_wrapper.decorate(self.refresh)

    def get_initial_query(self, override_query: Optional[QueryT] = None) -> QueryT:
        if override_query is not None:
            return override_query
        elif self.__initial_query is not None:
            return self.__initial_query
        else:
            raise NotImplementedError(
                "You must either pass the initial query or define get_initial_query()"
            )

    @abstractmethod
    def to_model(self, data: Dict[Any, Any]) -> ModelT:
        raise NotImplementedError()

    @abstractmethod
    def get(
        self,
        query: Optional[QueryT] = None,
    ) -> ModelT:
        """Return the one filtered object."""
        raise NotImplementedError("get() is not implemented()")

    @abstractmethod
    def get_by_id(
        self,
        id_value: Any
    ) -> ModelT:
        """Return the object by id."""

        raise NotImplementedError("get_by_id() is not implemented()")

    @abstractmethod
    def filter(
        self,
        query: Optional[QueryT] = None,
        **kwargs
    ) -> Collection[ModelT]:
        """Return the objects collection."""
        raise NotImplementedError("filter() is not implemented()")

    @abstractmethod
    def save(
        self, obj: Optional[ModelT] = None, obj_data: Optional[Dict] = None
    ) -> ModelT:
        """Save the object by filling it with ``obj_data``."""
        raise NotImplementedError("save() is not implemented in the repository")

    @abstractmethod
    def update(
        self,
        obj: Optional[ModelT] = None,
        query: Optional[QueryT] = None,
        update_values: Optional[Dict[Any, Any]] = None,
    ) -> None:
        raise NotImplementedError("update() is not implemented in the repository")

    @abstractmethod
    def delete(
        self,
        obj: Optional[ModelT] = None,
        query: Optional[QueryT] = None,
    ) -> None:
        """Delete the object."""
        raise NotImplementedError("delete() is not implemented in the repository")

    @abstractmethod
    def is_modified(self, obj: ModelT) -> bool:
        raise NotImplementedError("is_modified() is not implemented in the repository")

    @abstractmethod
    def refresh(self, obj: ModelT) -> None:
        raise NotImplementedError("refresh() is not implemented in the repository")


class AsyncRepository(Generic[SessionT, ModelT, QueryT], ABC):
    def __init__(
        self,
        session: AsyncSessionT,
        model: Type[ModelT],
        initial_query: Optional[QueryT] = None,
    ):
        self.session = session
        self.model = model
        self.__initial_query: Optional[QueryT] = initial_query

    def get_initial_query(self, override_query: Optional[QueryT] = None) -> QueryT:
        """Return the query (initial or overriding)."""
        if override_query is not None:
            return override_query
        elif self.__initial_query is not None:
            return self.__initial_query
        else:
            raise NotImplementedError(
                "You must either pass the initial query or define get_initial_query()"
            )

    @abstractmethod
    def to_model(self, data: Dict[Any, Any]) -> ModelT:
        """Converts data from Python dictionaries to models that Repository uses."""
        raise NotImplementedError()

    @abstractmethod
    async def get(
        self,
        query: Optional[QueryT] = None,
    ) -> ModelT:
        """Return the one filtered object."""
        raise NotImplementedError("get() is not implemented()")

    @abstractmethod
    async def get_by_id(
        self,
        id_value: Any
    ) -> ModelT:
        """Return the object by id."""

        raise NotImplementedError("get_by_id() is not implemented()")

    @abstractmethod
    async def filter(
        self,
        query: Optional[QueryT] = None,
        **filters,
    ) -> Collection[ModelT]:
        """Return the objects collection."""
        raise NotImplementedError("filter() is not implemented()")

    @abstractmethod
    async def save(
        self, obj: Optional[ModelT] = None, obj_data: Optional[Dict] = None
    ) -> ModelT:
        """Save the object by filling it with ``obj_data``."""
        raise NotImplementedError("save() is not implemented in the repository")

    @abstractmethod
    async def update(
        self,
        model: ModelT,
        update_values: Dict[Any, Any],
    ) -> ModelT:
        raise NotImplementedError("update() is not implemented in the repository")

    @abstractmethod
    async def update_many(
        self,
        query: QueryT,
        update_values: Dict[Any, Any],
    ) -> None:
        raise NotImplementedError("update() is not implemented in the repository")

    @abstractmethod
    async def delete(
        self,
        model: ModelT
    ) -> None:
        """Delete the object."""
        raise NotImplementedError("delete() is not implemented in the repository")

    @abstractmethod
    async def delete_many(
        self,
        query: QueryT,
    ) -> None:
        """Delete the object."""
        raise NotImplementedError("delete() is not implemented in the repository")

    @abstractmethod
    def is_modified(self, obj: ModelT) -> bool:
        raise NotImplementedError("is_modified() is not implemented in the repository")

    @abstractmethod
    async def refresh(self, obj: ModelT) -> None:
        raise NotImplementedError("refresh() is not implemented in the repository")
