"""Классы схем для прложения ``categories``."""

from typing import Optional

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CategoryCreateSchema(BaseModel):
    name: str
    parent_id: Optional[int] = None
    description: Optional[str] = None
    created_by: Optional[int] = None

class CategoryReadSchema(BaseModel):
    id: int
    name: str
    parent_id: Optional[int] = None
    description: Optional[str] = None
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class CategoryUpdateSchema(BaseModel):
    name: str
    parent_id: Optional[int] = None
    description: Optional[str] = None
