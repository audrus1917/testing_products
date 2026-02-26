"""``dependencies`` для приложения ``orders``."""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.alchemy import get_session
from src.database.alchemy.unit_of_work import AlchemyUnitOfWork

from src.apps.orders.models import Order
from src.apps.orders.repositories import OrderRepository
from src.apps.orders.services import OrderService


async def get_repository(
    session: AsyncSession = Depends(get_session),
):
    yield OrderRepository(session=session, model=Order)


async def _get_uow(session: AsyncSession = Depends(get_session)):
    yield AlchemyUnitOfWork(session=session)


async def get_service(
    uow=Depends(_get_uow),
    repository=Depends(get_repository)
):
    yield OrderService(uow=uow, repository=repository)


__all__ = ['get_service']
