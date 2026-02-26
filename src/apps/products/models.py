"""Классы моделей приложения ``products``."""

from __future__ import annotations
from typing import TYPE_CHECKING

from decimal import Decimal

from sqlalchemy import String, Text, Integer, Numeric, ForeignKey

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from src.database.alchemy import Base
from src.database.alchemy.mixins import JSONMixin, ChangedAtMixin

if TYPE_CHECKING:
    from src.apps.users.models import User
    from src.apps.manufacturers.models import Manufacturer


class Product(
    ChangedAtMixin,
    JSONMixin,
    Base
):
    __tablename__ = "products"

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
    price: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
        default=0.,
        doc="Цена продукта"
    )
    created_by: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )
    manufacturer_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("manufacturers.id"),
        nullable=True
    )
    author = relationship(
        "User",
        lazy="select",
        uselist=False
    )
    manufacturer = relationship(
        "Manufacturer",
        lazy="select",
        uselist=False
    )

    def __repr__(self) -> str:
        return f"Product(id={self.id}, name={self.name})"
