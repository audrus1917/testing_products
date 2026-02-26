"""``dependencies`` для приложения ``products``."""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.alchemy import get_session
from src.database.alchemy.unit_of_work import AlchemyUnitOfWork

from src.apps.products.models import Product
from src.apps.products.repositories import ProductRepository
from src.apps.products.services import ProductService


async def get_repository(
    session: AsyncSession = Depends(get_session),
):
    yield ProductRepository(session=session, model=Product)


async def _get_uow(session: AsyncSession = Depends(get_session)):
    yield AlchemyUnitOfWork(session=session)


async def get_service(
    uow=Depends(_get_uow),
    repository=Depends(get_repository)
):
    yield ProductService(uow=uow, repository=repository)


__all__ = ['get_service']
