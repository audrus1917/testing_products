"""`Dataclass` для приложение `Категории`."""

import uuid

from datetime import datetime
from dataclasses import dataclass
from typing import Optional


@dataclass
class CategoryEntity:

    name: str
    id: Optional[uuid.UUID] = None
    parent_id: Optional[uuid.UUID] = None
    description: Optional[str] = None
    created_by: Optional[int] = None
    created_at: Optional[datetime] = None
