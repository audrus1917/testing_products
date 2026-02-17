"""The service for ``Person`` entity."""

from src.core.services.crud import AsyncCRUDService

from .models import PersonModel


class PersonService[PersonModel](AsyncCRUDService):
    pass
