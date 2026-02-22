"""``dependencies`` для приложения :app:`users`."""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.alchemy import get_session
from src.database.alchemy.unit_of_work import AlchemyUnitOfWork

from src.apps.categories.models import Category
from src.apps.categories.repositories import CategoryRepository
from src.apps.categories.services import CategoryService


async def get_repository(
    session: AsyncSession = Depends(get_session),
):
    yield CategoryRepository(session=session, model=Category)


async def _get_uow(session: AsyncSession = Depends(get_session)):
    yield AlchemyUnitOfWork(session=session)


async def get_service(
    uow=Depends(_get_uow),
):
    yield CategoryService(uow=uow)


__all__ = ['get_service']
