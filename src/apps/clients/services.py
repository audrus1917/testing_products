from src.core.services.crud import AsyncCRUDService

from src.apps.clients.models import Client
from src.apps.clients.repositories import ClientRepository


class ClientService(AsyncCRUDService):
    repository = ClientRepository
