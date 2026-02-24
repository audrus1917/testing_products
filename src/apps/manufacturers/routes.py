from __future__ import annotations

import logging

from fastapi import APIRouter, status, Depends

from src.core.utils import schema_model_dump

from src.oauth2.tokens import get_current_user

from src.apps.manufacturers.models import Manufacturer
from src.apps.manufacturers.schemas import (
    ManufacturerCreateSchema,
    ManufacturerReadSchema,
    ManufacturerUpdateSchema
)
from src.apps.manufacturers.services import ManufacturerService
from src.apps.manufacturers.depends import get_service

logger = logging.getLogger(__name__)

manufacturers_router = APIRouter(
    tags=["manufacturers"]
)

@manufacturers_router.post(
    "/",
    response_model=ManufacturerReadSchema,
    status_code=status.HTTP_201_CREATED,
    description="Добавление нового производителя"
)
async def create_manufacturer(
    manufacturer_data: ManufacturerCreateSchema,
    service: ManufacturerService = Depends(get_service),
    user_id: int = Depends(get_current_user)
) -> ManufacturerReadSchema:
    """Добавляет нового производителя."""

    if user_id:
        manufacturer_data.created_by = user_id
    model = await service.create(obj_data=schema_model_dump(manufacturer_data))
    return ManufacturerReadSchema.model_validate(model)


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


@manufacturers_router.patch(
    "/{manufacturer_id}",
    response_model=ManufacturerReadSchema,
    description="Обновление данных о производителе"
)
async def update_manufacturer(
    manufacturer_id: int,
    manufacturer_data: ManufacturerUpdateSchema,
    service: ManufacturerService = Depends(get_service)
) -> ManufacturerReadSchema:
    """Обновляет данные о производителе."""

    model = await service.update(
        query={"id": manufacturer_id},
        update_values=schema_model_dump(manufacturer_data),
    )
    return ManufacturerReadSchema.model_validate(model)
