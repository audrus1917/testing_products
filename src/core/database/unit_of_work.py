"""Абстрактный класс для ``Unit of Work``."""

from abc import ABC, abstractmethod
from typing import Optional, TypeVar

from src.core.error_wrapper import ErrorWrapper


SessionT = TypeVar("SessionT")
AsyncSessionT = TypeVar("AsyncSessionT")


class UnitOfWork[SessionT](ABC):
    error_wrapper: ErrorWrapper = ErrorWrapper()

    def __init__(
        self,
        session: SessionT,
        autocommit: Optional[bool] = False,
    ):
        self.session = session
        self.autocommit = autocommit

    @abstractmethod
    def begin(self):
        raise NotImplementedError()

    @abstractmethod
    def rollback(self):
        raise NotImplementedError()

    @abstractmethod
    def commit(self):
        raise NotImplementedError()

    @abstractmethod
    def close(self):
        raise NotImplementedError()

    def __enter__(self):
        self.begin()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.rollback()
            self.close()
            raise exc_val
        else:
            if self.autocommit:
                self.commit()

            self.close()

    def __str__(self):
        return f"{self.__class__.__name__}"

    def __repr__(self):
        return str(self)


class AsyncUnitOfWork[AsyncSessionT](ABC):
    error_wrapper: ErrorWrapper = ErrorWrapper()

    def __init__(
        self,
        session: AsyncSessionT,
        autocommit: Optional[bool] = False,
    ):
        self.session = session
        self.autocommit = autocommit

    @abstractmethod
    async def begin(self):
        raise NotImplementedError()

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError()

    @abstractmethod
    async def commit(self):
        raise NotImplementedError()

    @abstractmethod
    async def close(self):
        raise NotImplementedError()

    async def __aenter__(self):
        await self.begin()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            await self.rollback()
            await self.close()
            raise exc_val
        else:
            if self.autocommit:
                await self.commit()
            await self.close()

    def __str__(self):
        return f"{self.__class__.__name__}"

    def __repr__(self):
        return str(self)


__all__ = [
    "UnitOfWork",
    "AsyncUnitOfWork"
]
