"""Датакласс для модели ``User``."""

from datetime import datetime
from dataclasses import dataclass
from typing import Optional


@dataclass
class CategoryEntity:

    name: str
    id: Optional[int] = None
    parent_id: Optional[int] = None
    description: Optional[str] = None
    created_by: Optional[int] = None
    created_at: Optional[datetime] = None
