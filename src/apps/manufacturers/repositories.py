"""Репозиторий приложения ``manufacturers``."""

from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import aliased
from sqlalchemy.engine import Row

from src.database.alchemy.repositories import AlchemyRepository
from src.apps.manufacturers.models import Manufacturer


class ManufacturerRepository(AlchemyRepository):
    """Класс репозитория для работы с производителями."""

    model = Manufacturer

