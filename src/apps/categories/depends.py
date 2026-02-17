"""``dependencies`` для приложения :app:`users`."""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.persons.models import PersonModel
from src.database.alchemy import get_session
from src.database.alchemy.unit_of_work import AlchemyUnitOfWork

from .repositories import PersonRepository
from .services import PersonService
from .controllers import PersonController


async def get_repository(
    session: AsyncSession = Depends(get_session),
):
    yield PersonRepository(session=session, model=PersonModel)


async def _get_uow(session: AsyncSession = Depends(get_session)):
    yield AlchemyUnitOfWork(session=session)


async def get_service(
    uow=Depends(_get_uow),
):
    yield PersonService(uow=uow)


async def get_controller(
    person_service=Depends(get_service),
):
    yield PersonController(person_service=person_service)


__all__ = ['get_controller', 'get_service']
