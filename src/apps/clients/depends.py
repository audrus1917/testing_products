"""``dependencies`` для приложения ``clients``."""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.alchemy import get_session
from src.database.alchemy.unit_of_work import AlchemyUnitOfWork

from src.apps.clients.models import Client
from src.apps.clients.repositories import ClientRepository
from src.apps.clients.services import ClientService


async def get_repository(
    session: AsyncSession = Depends(get_session),
):
    yield ClientRepository(session=session, model=Client)


async def _get_uow(session: AsyncSession = Depends(get_session)):
    yield AlchemyUnitOfWork(session=session)


async def get_service(
    uow=Depends(_get_uow),
    repository=Depends(get_repository)
):
    yield ClientService(uow=uow, repository=repository)


__all__ = ['get_service']
