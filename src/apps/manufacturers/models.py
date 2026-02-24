"""Классы моделей приложения ``manufacturers``."""

from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import String, Text, Integer, ForeignKey
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from src.database.alchemy import Base
from src.database.alchemy.mixins import JSONMixin, ChangedAtMixin

if TYPE_CHECKING:
    from src.apps.users.models import User


class Manufacturer(
    ChangedAtMixin,
    JSONMixin,
    Base
):
    __tablename__ = "manufacturers"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
        doc="Наименование"
    )
    description: Mapped[str] = mapped_column(
        Text,
        nullable=True,
        doc="Описание"
    )
    created_by: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )
    author = relationship(
        "User",
        lazy="select",
        uselist=False
    )

    def __repr__(self) -> str:
        return f"Manufacturer(id={self.id}, name={self.name})"
