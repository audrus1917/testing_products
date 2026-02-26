from __future__ import annotations
from typing import Optional

import logging

from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from fastapi_filter import FilterDepends
from fastapi_filter.contrib.sqlalchemy import Filter

from src.core.utils import schema_model_dump
from src.oauth2.tokens import get_current_user, UserData 
from src.core.http_response_schemas import Unauthorized

from src.apps.api_error_wrapper import api_error_wrapper
from src.apps.orders.models import Order
from src.apps.orders.schemas import (
    OrderCreateSchema,
    OrderReadSchema,
    OrderUpdateSchema,
    OrderListSchema,
    OrderItemCreateSchema,
    OrderItemReadSchema

)
from src.apps.orders.services import OrderService
from src.apps.orders.depends import get_service

logger = logging.getLogger(__name__)

orders_router = APIRouter(
    tags=["orders"]
)

class OrderFilter(Filter):
    name: Optional[str] = None
    name__like: Optional[str] = None

    class Constants(Filter.Constants):
        model = Order


@orders_router.get(
    "/",
    response_model=OrderListSchema,
    description="Получение списка заказов"
)
@api_error_wrapper.decorate
async def get_order_list(
    service: OrderService = Depends(get_service),
    filters: OrderFilter = FilterDepends(OrderFilter)
) -> OrderListSchema:
    """Возвращает данные о заказах."""

    items, total = await service.filter(filters=filters)
    return OrderListSchema(**{"items": items, "total": total})


@orders_router.get(
    "/{order_id}",
    response_model=OrderReadSchema,
    description="Получение детализированных данных о заказе"
)
@api_error_wrapper.decorate
async def get_order(
    order_id: int,
    service: OrderService = Depends(get_service),
) -> OrderReadSchema:
    """Возвращает данные о заказе."""

    model = await service.get_by_id(order_id)
    return OrderReadSchema.model_validate(model)


@orders_router.post(
    "/",
    response_model=OrderReadSchema,
    status_code=status.HTTP_201_CREATED,
    description="Добавление нового заказа"
)
@api_error_wrapper.decorate
async def create_order(
    order_data: OrderCreateSchema,
    service: OrderService = Depends(get_service),
    _: UserData = Depends(get_current_user)
) -> OrderReadSchema:
    """Добавляет новый заказ."""

    model = await service.create(obj_data=schema_model_dump(order_data))
    return OrderReadSchema.model_validate(model)


@orders_router.patch(
    "/{order_id}",
    response_model=OrderReadSchema,
    description="Обновление данных о заказе"
)
@api_error_wrapper.decorate
async def update_order(
    order_id: int,
    order_data: OrderUpdateSchema,
    service: OrderService = Depends(get_service),
    user_data: UserData = Depends(get_current_user)
) -> OrderReadSchema:
    """Обновляет данные о заказе."""
    model = await service.get_by_id(order_id)
    if not model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Заказ не найден"
        )

    updated_model = await service.update(
        model=model,
        update_values=schema_model_dump(order_data),
    )
    return OrderReadSchema.model_validate(updated_model)


@orders_router.delete(
    "/{order_id}",
    description='Удалить заказ',
    responses={
        status.HTTP_204_NO_CONTENT: {'description': 'Заказ успешно удален.'},
        status.HTTP_401_UNAUTHORIZED: {'model': Unauthorized},
    },
    status_code=status.HTTP_204_NO_CONTENT,
)
@api_error_wrapper.decorate
async def delete_order(
    order_id: int,
    service: OrderService = Depends(get_service),
    user_data: UserData = Depends(get_current_user)
):
    if not user_data.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав для выполнения операции"
        )

    await service.delete(order_id=order_id)


@orders_router.post(
    "/{order_id}/items/add",
    response_model=OrderReadSchema,
    status_code=status.HTTP_201_CREATED,
    description="Добавление нового товара в заказ"
)
@api_error_wrapper.decorate
async def add_item(
    order_id: int,
    order_item_data: OrderItemCreateSchema,
    service: OrderService = Depends(get_service),
) -> OrderReadSchema:
    """Добавляет новый товар в заказ."""

    order_model = await service.get_by_id(order_id)
    if not order_model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Заказ не найден"
        )

    updated_order_model = await service.add_item(
        model=order_model,
        obj_data=schema_model_dump(order_item_data)
    )
    result = OrderReadSchema.model_validate(updated_order_model)
    return result
