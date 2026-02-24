from src.core.services.crud import AsyncCRUDService

from src.apps.manufacturers.models import Manufacturer
from src.apps.manufacturers.repositories import ManufacturerRepository


class ManufacturerService(AsyncCRUDService):
    repository = ManufacturerRepository