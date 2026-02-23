from src.core.services.crud import AsyncCRUDService

from src.apps.users.models import User


class UserService[User](AsyncCRUDService):
    pass
