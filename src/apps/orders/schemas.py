"""Классы схем для приложения ``clients``."""

from typing import Optional

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from src.apps.orders.enums import OrderStatus, DeliveryMethod


class OrderCreateSchema(BaseModel):
    order_no: str = Field(..., title="Номер заказа")
    client_id: int = Field(..., title="ID клиента")
    delivery_method: DeliveryMethod = Field(..., title="Способ доставки")


class OrderReadSchema(BaseModel):
    id: int = Field(..., title="ID заказа")
    order_no: str = Field(..., title="Номер заказа")
    client_id: int = Field(..., title="ID клиента")
    registeration_date: Optional[datetime] = Field(
        None, title="Дата регистрации заказа"
    )
    payment_date: Optional[datetime] = Field(None, title="Дата оплаты заказа")
    delivery_date: Optional[datetime] = Field(
        None, 
        title="Дата доставки заказа"
    )
    delivery: Optional[DeliveryMethod] = Field(None, title="Способ доставки")
    status: Optional[OrderStatus] = Field(..., title="Статус заказа")

    model_config = ConfigDict(from_attributes=True)


class OrderUpdateSchema(BaseModel):
    delivery_method: Optional[DeliveryMethod] = Field(None, title="Способ доставки")
    payment_date: Optional[datetime] = Field(None, title="Дата оплаты заказа")
    delivery_date: Optional[datetime] = Field(
        None, 
        title="Дата доставки заказа"
    )


class OrderListSchema(BaseModel):
    items: list[OrderReadSchema]
    total: int


class OrderItemCreateSchema(BaseModel):
    order_id: int = Field(..., title="ID заказа")
    product_id: int = Field(..., title="ID продукта")
    amount: Decimal = Field(..., description="Количество")
    price: Optional[Decimal] = Field(None, description="Цена")


class OrderItemReadSchema(BaseModel):
    id: int = Field(..., title="ID позиции заказа")
    order_id: int = Field(..., title="ID заказа")
    product_id: int = Field(..., title="ID продукта")
    amount: Decimal = Field(..., description="Количество")
    price: Decimal = Field(..., description="Цена")

    model_config = ConfigDict(from_attributes=True)


class OrderItemUpdateSchema(BaseModel):
    amount: Optional[Decimal] = Field(None, description="Количество")
