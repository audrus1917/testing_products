"""Классы схем для приложения ``products``."""

from typing import Optional

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ProductCreateSchema(BaseModel):
    name: str
    description: Optional[str] = None
    created_by: Optional[int] = None

class ProductReadSchema(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class ProductUpdateSchema(BaseModel):
    name: str
    description: Optional[str] = None


class ProductListSchema(BaseModel):
    items: list[ProductReadSchema]
    total: int


