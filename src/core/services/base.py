"""Абстрактные классы для сервисов (синхронных и асинхронных)."""

from abc import ABC


class Service(ABC):
    pass


class AsyncService(ABC):
    pass


__all__ = ['Service', 'AsyncService']
