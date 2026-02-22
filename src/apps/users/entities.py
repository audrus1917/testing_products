"""Датакласс для модели ``User``."""

from datetime import datetime
from dataclasses import dataclass
from typing import Optional


@dataclass
class UserEntity:

    email: str
    hashed_password: str
    is_active: bool = True
    is_superuser: bool = False
    created_at: Optional[datetime] = None
