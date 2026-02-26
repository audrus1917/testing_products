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

from src.apps.manufacturers.models import Manufacturer
from src.apps.manufacturers.schemas import (
    ManufacturerCreateSchema,
    ManufacturerReadSchema,
    ManufacturerUpdateSchema,
    ManufacturerListSchema,
)
from src.apps.manufacturers.services import ManufacturerService
from src.apps.manufacturers.depends import get_service

logger = logging.getLogger(__name__)

manufacturers_router = APIRouter(
    tags=["manufacturers"]
)

class ManufacturerFilter(Filter):
    name: Optional[str] = None
    name__like: Optional[str] = None

    class Constants(Filter.Constants):
        model = Manufacturer


@manufacturers_router.get(
    "/",
    response_model=ManufacturerListSchema,
    description="Получение списка производителей"
)
async def get_manufacturer_list(
    service: ManufacturerService = Depends(get_service),
    filters: ManufacturerFilter = FilterDepends(ManufacturerFilter)
) -> ManufacturerListSchema:
    """Возвращает данные о производителях."""

    items, total = await service.filter(filters=filters)
    return ManufacturerListSchema(**{"items": items, "total": total})


@manufacturers_router.get(
    "/{manufacturer_id}",
    response_model=ManufacturerReadSchema,
    description="Получение детализированных данных о производителе"
)
async def get_manufacturer(
    manufacturer_id: int,
    service: ManufacturerService = Depends(get_service),
) -> ManufacturerReadSchema:
    """Возвращает данные о производителе."""

    model = await service.get_by_id(manufacturer_id)
    return ManufacturerReadSchema.model_validate(model)


@manufacturers_router.post(
    "/",
    response_model=ManufacturerReadSchema,
    status_code=status.HTTP_201_CREATED,
    description="Добавление нового производителя"
)
async def create_manufacturer(
    manufacturer_data: ManufacturerCreateSchema,
    service: ManufacturerService = Depends(get_service),
    user_data: UserData = Depends(get_current_user)
) -> ManufacturerReadSchema:
    """Добавляет нового производителя."""

    if not user_data.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав для выполнения операции"
        )
    
    manufacturer_data.created_by = user_data.user_id
    model = await service.create(obj_data=schema_model_dump(manufacturer_data))
    return ManufacturerReadSchema.model_validate(model)


@manufacturers_router.patch(
    "/{manufacturer_id}",
    response_model=ManufacturerReadSchema,
    description="Обновление данных о производителе"
)
async def update_manufacturer(
    manufacturer_id: int,
    manufacturer_data: ManufacturerUpdateSchema,
    service: ManufacturerService = Depends(get_service),
    user_data: UserData = Depends(get_current_user)
) -> ManufacturerReadSchema:
    """Обновляет данные о производителе."""
    if not user_data.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав для выполнения операции"
        )

    model = await service.update(
        query={"id": manufacturer_id},
        update_values=schema_model_dump(manufacturer_data),
    )
    return ManufacturerReadSchema.model_validate(model)


@manufacturers_router.delete(
    "/{manufacturer_id}",
    description='Удалить производителя',
    responses={
        status.HTTP_204_NO_CONTENT: {'description': 'Производитель успешно удален.'},
        status.HTTP_401_UNAUTHORIZED: {'model': Unauthorized},
    },
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_manufacturer(
    manufacturer_id: int,
    service: ManufacturerService = Depends(get_service),
    user_data: UserData = Depends(get_current_user)
):
    if not user_data.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав для выполнения операции"
        )

    await service.delete(manufacturer_id=manufacturer_id)
