"""Классы моделей приложения ``Clients``."""

from __future__ import annotations
from typing import TYPE_CHECKING

from decimal import Decimal

from sqlalchemy import String, Text, Integer, Numeric
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from src.database.alchemy import Base
from src.database.alchemy.mixins import JSONMixin, ChangedAtMixin

if TYPE_CHECKING:
    from src.apps.users.models import User


class Client(
    ChangedAtMixin,
    JSONMixin,
    Base
):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )
    last_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
        doc="Фамилия клиента"
    )
    first_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
        doc="Имя клиента"
    )
    address: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        index=True,
        doc="Адрес клиента"
    )
    phone: Mapped[str] = mapped_column(
        String(length=32),
        nullable=True,
        index=True,
        doc="Номер телефона клиента"
    )
    balance: Mapped[Decimal] = mapped_column(
        Numeric(15, 2),
        nullable=False,
        default=0.,
        doc="Баланс клиента"
    )

    @property
    def full_name(self) -> str:
        return f"{self.last_name} {self.first_name}"

    def __repr__(self) -> str:
        return f"Client(id={self.id}, last_name={self.last_name}, first_name={self.first_name}"


