from __future__ import annotations

from typing import Optional

import logging

from fastapi.exceptions import HTTPException
from fastapi import APIRouter, status, Depends
from fastapi_filter import FilterDepends
from fastapi_filter.contrib.sqlalchemy import Filter

from src.core.http_response_schemas import Unauthorized
from src.core.utils import schema_model_dump

from src.oauth2.tokens import get_current_user, UserData
from src.apps.api_error_wrapper import api_error_wrapper
from src.apps.categories.schemas import (
    CategoryCreateSchema,
    CategoryReadSchema,
    CategoryUpdateSchema,
    CategoryListSchema
)
from src.apps.categories.models import Category
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
@api_error_wrapper.decorate
async def create_category(
    category_data: CategoryCreateSchema,
    service: CategoryService = Depends(get_service),
    user_data: UserData = Depends(get_current_user)
) -> CategoryReadSchema:
    """Добавляет новую категорию."""

    if not user_data.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав для выполнения операции"
        )

    category_data.created_by = user_data.user_id
    model = await service.create(obj_data=schema_model_dump(category_data))
    return CategoryReadSchema.model_validate(model)


class CategoryFilter(Filter):
    name: Optional[str] = None
    name__like: Optional[str] = None

    class Constants(Filter.Constants):
        model = Category


@categories_router.get(
    "/",
    response_model=CategoryListSchema,
    description="Получение списка категорий"
)
@api_error_wrapper.decorate
async def get_manufacturer_list(
    service: CategoryService = Depends(get_service),
    filters: CategoryFilter = FilterDepends(CategoryFilter)
) -> CategoryListSchema:
    """Возвращает данные о производителях."""

    items, total = await service.filter(filters=filters)
    return CategoryListSchema(**{"items": items, "total": total})


@categories_router.get(
    "/{category_id}",
    response_model=CategoryReadSchema,
    description="Получение детализированных данных о категории"
)
@api_error_wrapper.decorate
async def get_category(
    category_id: int,
    service: CategoryService = Depends(get_service),
) -> CategoryReadSchema:
    """Возвращает данные о категории."""

    model = await service.get_by_id(category_id)
    return CategoryReadSchema.model_validate(model)



@categories_router.patch(
    "/{category_id}",
    response_model=CategoryReadSchema,
    description="Обновление данных о категории"
)
@api_error_wrapper.decorate
async def update_category(
    category_id: int,
    category_data: CategoryUpdateSchema,
    service: CategoryService = Depends(get_service),
    user_data: UserData = Depends(get_current_user)
) -> CategoryReadSchema:
    """Обновляет данные о категории."""
    if not user_data.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав для выполнения операции"
        )

    model = await service.get_by_id(category_id)
    if model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Категория с id {category_id} не найдена"
        )
    
    updated_model = await service.update(
        model=model,
        update_values=schema_model_dump(category_data)
    )
    return CategoryReadSchema.model_validate(updated_model)


@categories_router.delete(
    "/{category_id}",
    description='Удалить категорию',
    responses={
        status.HTTP_204_NO_CONTENT: {'description': 'Категория успешно удалена.'},
        status.HTTP_401_UNAUTHORIZED: {'model': Unauthorized},
    },
    status_code=status.HTTP_204_NO_CONTENT,
)
@api_error_wrapper.decorate
async def delete_category(
    category_id: int,
    service: CategoryService = Depends(get_service),
    user_data: UserData = Depends(get_current_user)
):
    if not user_data.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав для выполнения операции"
        )

    await service.delete(category_id=category_id)
