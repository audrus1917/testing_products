"""Репозиторий приложения ``manufacturers``."""


from src.database.alchemy.repositories import AlchemyRepository
from src.apps.manufacturers.models import Manufacturer


class ManufacturerRepository(AlchemyRepository):
    """Класс репозитория для работы с производителями."""

    model = Manufacturer

