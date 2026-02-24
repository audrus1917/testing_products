from __future__ import annotations

from typing import Optional

import logging

from fastapi.exceptions import HTTPException
from fastapi import APIRouter, status, Depends, Request
from fastapi_cache.decorator import cache

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.http_response_schemas import UniqueConstraint, Unauthorized
from src.core.exceptions import UniqueConstraintError
from src.core.utils import schema_model_dump

from src.oauth2.tokens import get_current_user
from src.database.alchemy import get_session

from src.apps.categories.models import Category
from src.apps.categories.schemas import (
    CategoryCreateSchema,
    CategoryReadSchema,
    CategoryUpdateSchema
)
from src.apps.categories.services import CategoryService
from src.apps.categories.depends import get_service

logger = logging.getLogger(__name__)

categories_router = APIRouter(
    tags=["categories"]
)

@categories_router.post(
    "/",
    response_model=CategoryReadSchema,
    status_code=status.HTTP_201_CREATED,
    description="Добавление новой категории"
)
async def create_category(
    category_data: CategoryCreateSchema,
    service: CategoryService = Depends(get_service),
    user_id: int = Depends(get_current_user)
) -> CategoryReadSchema:
    """Добавляет новую категорию."""
    if user_id:
        category_data.created_by = user_id
    model = await service.create(obj_data=schema_model_dump(category_data))
    return CategoryReadSchema.model_validate(model)


# @orders_router.get(
#     "/{order_id}",
#     response_model=OrderRead,
#     description="Получение детализированных данных о заказе"
# )
# @cache(
#     expire=settings.APPLICATION.CACHE_TTL * 60,
#     key_builder=custom_key_builder
# )
# async def get_order(
#     session: AsyncSession = Depends(get_session),
#     order: Order = Depends(get_order_by_id),
#     user: User = Depends(get_current_user),
# ) -> OrderRead:
#     """Возвращает данные о заказе."""

#     return OrderRead.model_validate(order, from_attributes=True)


# @orders_router.patch(
#     "/{order_id}",
#     response_model=OrderRead,
#     description="Добавление нового заказа"
# )
# async def update_order_status(
#     order_status_data: OrderUpdateStatus,
#     order_model: Order = Depends(get_order_by_id),
#     session: AsyncSession = Depends(get_session),
#     _: User = Depends(get_current_user)
# ) -> Order:
#     """Добавляет новый ордер."""

#     if order_model and order_model.status != order_status_data.status:
#         order_model.status = order_status_data.status
#         try:
#             await session.commit()
#         except SQLAlchemyError as exc:
#             response_data = {
#                 "status_code": status.HTTP_400_BAD_REQUEST,
#                 "detail": f"Ошибка SQLAlchemy: {exc}"
#             }
#             raise HTTPException(**response_data) from exc
#     return order_model


# @orders_router.get(
#     "/user/{user_id}",
#     response_model=OrderListRead,
#     description="Список заказов пользователя"
# )
# async def get_user_orders(
#     user_model: User = Depends(get_user_by_id),
#     session: AsyncSession = Depends(get_session),
#     user: User = Depends(get_current_user),
# ):
#     """Возвращает cписок заказов пользователя."""

#     if not user.is_superuser:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Недостаточно прав"
#         )

#     stmt = select(Order).where(Order.user_id == user_model.id)
#     result = await session.execute(stmt)
#     rows = result.scalars()
#     items = [OrderRead.model_validate(rows) for rows in rows]
#     return {"items": items, "total": len(items)}
