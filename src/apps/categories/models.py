"""Классы моделей приложения ``categories``."""

from __future__ import annotations

from sqlalchemy import String, Text, Integer, ForeignKey
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from src.database.alchemy import Base
from src.database.alchemy.mixins import JSONMixin, ChangedAtMixin

from src.apps.users.models import User


class Category(
    ChangedAtMixin,
    JSONMixin,
    Base
):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )
    parent_id = mapped_column(
        Integer,
        ForeignKey("categories.id"),
        nullable=True
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
        deferred=True,
        doc="Описание"
    )
    created_by: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )
    children = relationship(
        "Category",
        back_populates="parent",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    parent = relationship(
        "Category",
        back_populates="children",
        remote_side=[id]
    )
    author = relationship(
        "User",
        lazy="select",
        uselist=False
    )

    def __repr__(self) -> str:
        return f"Category(id={self.id}, name={self.name}, parent={self.parent_id})"
