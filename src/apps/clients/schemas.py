"""Классы схем для приложения ``clients``."""

from typing import Optional

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ClientCreateSchema(BaseModel):
    last_name: str
    first_name: str
    address: str
    phone: Optional[str] = None

class ClientReadSchema(BaseModel):
    id: int
    last_name: str
    first_name: str
    address: str
    phone: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class ClientUpdateSchema(BaseModel):
    last_name: Optional[str] = None
    first_name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None


class ClientListSchema(BaseModel):
    items: list[ClientReadSchema]
    total: int


