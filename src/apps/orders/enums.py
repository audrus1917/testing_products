"""Перечисление для статуса заказа."""

from enum import Enum


class OrderStatus(str, Enum):
    """Возможный значения статуса заказа."""

    NOT_PAID = "Не оплачен"
    PAID = "Оплачен"
    IN_DELIVERY = "В доставке"
    DELIVERED = "Доставлен"
    CANCELED = "Отменен"


class DeliveryMethod(str, Enum):
    DELIVERY = "Доставка"
    EXPRESS_DELIVERY = "Экспресс доставка"

