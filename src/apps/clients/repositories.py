"""Репозиторий приложения ``clients``."""


from src.database.alchemy.repositories import AlchemyRepository
from src.apps.clients.models import Client


class ClientRepository(AlchemyRepository):
    """Класс репозитория для работы с клиентами."""

    model = Client
