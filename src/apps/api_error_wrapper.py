"""Обертка для ошибок."""

from fastapi.exceptions import HTTPException
from src.core.error_wrapper import ErrorWrapper
from src.core.exceptions import NotFoundError
from src.core.database.exceptions import InvalidQueryError


api_error_wrapper = ErrorWrapper(
    error_mappings={
        NotFoundError: lambda error: HTTPException(status_code=404, detail="Not found"),
        InvalidQueryError: lambda error: HTTPException(status_code=400, detail="Invaild query"),
    },
    default_error=lambda error: HTTPException(status_code=500, detail="Unknown error"),
)
