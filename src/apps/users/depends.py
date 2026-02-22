"""``dependencies`` для приложения ``users``."""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.alchemy import get_session
from src.database.alchemy.unit_of_work import AlchemyUnitOfWork

from src.apps.users.models import User
from src.apps.users.repositories import UserRepository
from src.apps.users.services import UserService


async def get_repository(
    session: AsyncSession = Depends(get_session),
):
    yield UserRepository(session=session, model=User)


async def _get_uow(session: AsyncSession = Depends(get_session)):
    yield AlchemyUnitOfWork(session=session)


async def get_service(
    uow=Depends(_get_uow),
):
    yield UserService(uow=uow)


__all__ = ['get_service']
