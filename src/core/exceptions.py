class UniqueConstraintError(Exception):
    """Ограничение на уникальность объектов"""


class NotFoundError(Exception):
    """Страница/объект не найден(а)"""


class IsOwnerError(Exception):
    """Нет доступа к объекту."""
