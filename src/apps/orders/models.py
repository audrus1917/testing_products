"""Классы моделей приложения ``orders``."""

from __future__ import annotations
from typing import TYPE_CHECKING

from decimal import Decimal

from sqlalchemy import String, Text, Integer, Numeric, Date, Enum, ForeignKey

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from src.database.alchemy import Base
from src.database.alchemy.mixins import JSONMixin, ChangedAtMixin

from src.apps.orders.enums import OrderStatus, DeliveryMethod

if TYPE_CHECKING:
    from src.apps.users.models import User
    from src.apps.clients.models import Client
    from src.apps.products.models import Product


class Order(
    ChangedAtMixin,
    JSONMixin,
    Base
):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )
    order_no: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
        doc="Номер заказа"
    )
    client_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("clients.id"),
        nullable=True
    )
    registration_date: Mapped[Date] = mapped_column(
        Date,
        nullable=True,
        doc="Дата регистрации заказа"
    )
    payment_date: Mapped[Date] = mapped_column(
        Date,
        nullable=True,
        doc="Дата оплаты заказа"
    )
    delivery_date: Mapped[Date] = mapped_column(
        Date,
        nullable=True,
        doc="Дата доставки заказа"
    )
    status: Mapped[OrderStatus] = mapped_column(
        Enum(OrderStatus),
        nullable=False,
        default=OrderStatus.NOT_PAID,
        index=True,
        doc="Статус заказа"
    )
    delivery: Mapped[DeliveryMethod] = mapped_column(
        Enum(DeliveryMethod),
        nullable=False,
        default=DeliveryMethod.DELIVERY,
        index=True,
        doc="Способ доставки"
    )

    client = relationship(
        "Client",
        lazy="select",
        uselist=False
    )

    def __repr__(self) -> str:
        return (
            f"Order(id={self.id}, client={self.client.full_name}, "
            f"status={self.status})"
        )


#     product = models.ForeignKey(Product, verbose_name=_("продукт в заказе"), on_delete=models.CASCADE)
#     order = models.ForeignKey(Order, verbose_name=_("заказ"), on_delete=models.CASCADE)
#     price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("цена"))
#     amount = models.PositiveIntegerField(verbose_name=_("количество"), default=1)

class OrderItem(
    ChangedAtMixin,
    JSONMixin,
    Base
):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )
#     order_status = models.ForeignKey("OrderStatus", verbose_name=_("статус заказа"), on_delete=models.CASCADE)
#     delivery = models.ForeignKey("Delivery", verbose_name=_("доставка"), on_delete=models.CASCADE)

    product_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("products.id"),
        nullable=False
    )
    order_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("orders.id"),
        nullable=False
    )
    product = relationship(
        "Client",
        lazy="select",
        uselist=False
    )
    order = relationship(
        "Order",
        lazy="select",
        uselist=False
    )
    price: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
        default=0.,
        doc="Цена"
    )
    amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
        default=0,
        doc="Количество"
    )

    def __repr__(self) -> str:
        return (
            f"OrderItem(id={self.id}, product={self.product.name}, "
            f"order={self.order.id})"
        )
