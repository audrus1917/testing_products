"""Класс модели ``Категории``."""

from __future__ import annotations
from typing import TYPE_CHECKING

import uuid

from sqlalchemy import String, Text, Integer, ForeignKey
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
    backref,
    attribute_mapped_collection
)
from sqlalchemy.dialects.postgresql import UUID

from src.database.alchemy import Base
from src.database.alchemy.mixins import JSONRepresentationMixin, ChangedAtMixin

if TYPE_CHECKING:
    from src.apps.users.models import User


class Category(
    ChangedAtMixin,
    JSONRepresentationMixin,
    Base
):
    """Класс модели для пользователей."""

    __tablename__ = 'categories'

    id: Mapped[UUID] = mapped_column(
        UUID,
        primary_key=True,
        default=uuid.uuid4
    )
    parent_id = mapped_column(
        UUID,
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
    created_by: Mapped["User"] = relationship(
        "User",
        back_populates='categories',
        lazy='select',
        doc="Кем создано"
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

    def __repr__(self) -> str:
        return f"Category(id={self.id}, name={self.name})"
