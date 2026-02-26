"""The `User` and `Role` schemas."""

import re

from datetime import datetime
from typing import Optional

from pydantic import EmailStr, ConfigDict, field_validator, BaseModel
from pydantic_core import PydanticCustomError

PASSWORD_VALID_RE = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*]).{6,}$')
PASSWORD_INVALID_MSG = """Значение должно содержать:
* хотя бы одну строчную латинскую букву;
* хотя бы одну заглавную латинскую букву;
* хотя бы одну цифру;
* хотя бы один спецсимвол (!@#$%^&*).
"""


class PasswordMixin:
    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str):
        if not PASSWORD_VALID_RE.match(v):
            raise PydanticCustomError(
                'invalid_password_value',
                f"Неверное значение для поля 'Пароль'. {PASSWORD_INVALID_MSG}",
            )

        return v


class UserCreateSchema(PasswordMixin, BaseModel):

    email: EmailStr
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False


class UserReadSchema(BaseModel):
    id: int
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False

    model_config = ConfigDict(from_attributes=True)


class UserUpdateSchema(PasswordMixin, BaseModel):
    password: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
    last_login: Optional[datetime] = None
