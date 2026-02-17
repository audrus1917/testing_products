"""Классы схем для ``Person``."""

from typing import Optional, List, Union

from datetime import datetime

from pydantic import BaseModel, EmailStr, ConfigDict

from src.core.schemas import OwnFieldsOnlyMixin
from .enums import Gender


class PersonRegisterSchema(BaseModel):
    """Класс схемы для регистрации пользователя."""

    email: EmailStr
    password: str
    last_name: str
    first_name: str
    second_name: Optional[str] = None
    phone: str
    gender: Optional[Gender] = None
    birth_date: Optional[datetime] = None
    birth_place: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class PersonInSchema(OwnFieldsOnlyMixin, BaseModel):
    """The incoming data schema."""

    last_name: str
    first_name: str
    second_name: Optional[str] = None
    phone: str
    birth_date: Optional[datetime] = None
    birth_place: Optional[str] = None
    gender: Optional[Gender] = None

    model_config = ConfigDict(
        from_attributes=True,
        extra="allow"
    )


class PersonInTildaSchema(BaseModel):
    """The incoming data schema for request from `Tilda`."""

    test: str
    last_name: Optional[str] = None
    first_name: Optional[str] = None
    second_name: Optional[str] = None
    phone: Optional[str] = None
    birth_date: Optional[datetime] = None
    birth_place: Optional[str] = None
    gender: Optional[Gender] = None

    model_config = ConfigDict(from_attributes=True)


class PersonOutSchema(BaseModel):
    id: int
    last_name: str
    first_name: str
    second_name: Optional[str] = None
    phone: str
    birth_date: Optional[datetime] = None
    birth_place: Optional[str] = None
    gender: Optional[Gender] = None

    model_config = ConfigDict(from_attributes=True)


class PersonUpdateSchema(BaseModel):
    last_name: str
    first_name: str
    second_name: Optional[str] = None
    phone: str
    birth_date: datetime
    birth_place: Optional[str] = None
    gender: Optional[Gender] = None


class PersonsListSchema(BaseModel):
    items: List[PersonOutSchema]
    pages: int
    page: int
    per_page: int
    total: int


PersonSchemaT = Union[PersonRegisterSchema, PersonInTildaSchema, PersonInSchema]
