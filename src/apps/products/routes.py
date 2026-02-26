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

from src.apps.products.models import Product
from src.apps.products.schemas import (
    ProductCreateSchema,
    ProductReadSchema,
    ProductUpdateSchema,
    ProductListSchema,
)
from src.apps.products.services import ProductService
from src.apps.products.depends import get_service

logger = logging.getLogger(__name__)

products_router = APIRouter(
    tags=["products"]
)

class ProductFilter(Filter):
    name: Optional[str] = None
    name__like: Optional[str] = None

    class Constants(Filter.Constants):
        model = Product


@products_router.get(
    "/",
    response_model=ProductListSchema,
    description="Получение списка производителей"
)
async def get_product_list(
    service: ProductService = Depends(get_service),
    filters: ProductFilter = FilterDepends(ProductFilter)
) -> ProductListSchema:
    """Возвращает данные о производителях."""

    items, total = await service.filter(filters=filters)
    return ProductListSchema(**{"items": items, "total": total})


@products_router.get(
    "/{product_id}",
    response_model=ProductReadSchema,
    description="Получение детализированных данных о производителе"
)
async def get_product(
    product_id: int,
    service: ProductService = Depends(get_service),
) -> ProductReadSchema:
    """Возвращает данные о производителе."""

    model = await service.get_by_id(product_id)
    return ProductReadSchema.model_validate(model)


@products_router.post(
    "/",
    response_model=ProductReadSchema,
    status_code=status.HTTP_201_CREATED,
    description="Добавление нового производителя"
)
async def create_product(
    product_data: ProductCreateSchema,
    service: ProductService = Depends(get_service),
    user_data: UserData = Depends(get_current_user)
) -> ProductReadSchema:
    """Добавляет нового производителя."""

    if not user_data.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав для выполнения операции"
        )
    
    product_data.created_by = user_data.user_id
    model = await service.create(obj_data=schema_model_dump(product_data))
    return ProductReadSchema.model_validate(model)


@products_router.patch(
    "/{product_id}",
    response_model=ProductReadSchema,
    description="Обновление данных о производителе"
)
async def update_product(
    product_id: int,
    product_data: ProductUpdateSchema,
    service: ProductService = Depends(get_service),
    user_data: UserData = Depends(get_current_user)
) -> ProductReadSchema:
    """Обновляет данные о производителе."""
    if not user_data.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав для выполнения операции"
        )

    model = await service.update(
        query={"id": product_id},
        update_values=schema_model_dump(product_data),
    )
    return ProductReadSchema.model_validate(model)


@products_router.delete(
    "/{product_id}",
    description='Удалить производителя',
    responses={
        status.HTTP_204_NO_CONTENT: {'description': 'Производитель успешно удален.'},
        status.HTTP_401_UNAUTHORIZED: {'model': Unauthorized},
    },
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_product(
    product_id: int,
    service: ProductService = Depends(get_service),
    user_data: UserData = Depends(get_current_user)
):
    if not user_data.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав для выполнения операции"
        )

    await service.delete(product_id=product_id)
