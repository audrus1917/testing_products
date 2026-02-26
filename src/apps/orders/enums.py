"""Перечисление для статуса заказа."""

from enum import Enum


class OrderStatus(str, Enum):
    """Возможный значения статуса заказа."""

    NOT_PAID = "NOT_PAID"
    PAID = "PAID"
    IN_DELIVERY = "IN_DELIVERY"
    DELIVERED = "DELIVERED"
    CANCELED = "CANCELED"


class DeliveryMethod(str, Enum):
    DELIVERY = "DELIVERY"
    EXPRESS_DELIVERY = "EXPRESS_DELIVERY"

