"""Классы схем для приложения ``manufacturers``."""

from typing import Optional

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ManufacturerCreateSchema(BaseModel):
    name: str
    description: Optional[str] = None
    created_by: Optional[int] = None

class ManufacturerReadSchema(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class ManufacturerUpdateSchema(BaseModel):
    name: str
    description: Optional[str] = None


class ManufacturerListSchema(BaseModel):
    items: list[ManufacturerReadSchema]
    total: int


