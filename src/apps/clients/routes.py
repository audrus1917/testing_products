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

from src.apps.clients.models import Client
from src.apps.clients.schemas import (
    ClientCreateSchema,
    ClientReadSchema,
    ClientUpdateSchema,
    ClientListSchema,
)
from src.apps.clients.services import ClientService
from src.apps.clients.depends import get_service

logger = logging.getLogger(__name__)

clients_router = APIRouter(
    tags=["clients"]
)

class ClientFilter(Filter):
    name: Optional[str] = None
    name__like: Optional[str] = None

    class Constants(Filter.Constants):
        model = Client


@clients_router.get(
    "/",
    response_model=ClientListSchema,
    description="Получение списка клиентов"
)
async def get_client_list(
    service: ClientService = Depends(get_service),
    filters: ClientFilter = FilterDepends(ClientFilter)
) -> ClientListSchema:
    """Возвращает данные о клиентах."""

    items, total = await service.filter(filters=filters)
    return ClientListSchema(**{"items": items, "total": total})


@clients_router.get(
    "/{client_id}",
    response_model=ClientReadSchema,
    description="Получение детализированных данных о клиенте"
)
async def get_client(
    client_id: int,
    service: ClientService = Depends(get_service),
) -> ClientReadSchema:
    """Возвращает данные о клиенте."""

    model = await service.get_by_id(client_id)
    return ClientReadSchema.model_validate(model)


@clients_router.post(
    "/",
    response_model=ClientReadSchema,
    status_code=status.HTTP_201_CREATED,
    description="Добавление нового клиента"
)
async def create_client(
    client_data: ClientCreateSchema,
    service: ClientService = Depends(get_service),
    user_data: UserData = Depends(get_current_user)
) -> ClientReadSchema:
    """Добавляет нового клиента."""

    if not user_data.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав для выполнения операции"
        )
    
    client_data.created_by = user_data.user_id
    model = await service.create(obj_data=schema_model_dump(client_data))
    return ClientReadSchema.model_validate(model)


@clients_router.patch(
    "/{client_id}",
    response_model=ClientReadSchema,
    description="Обновление данных о клиенте"
)
async def update_client(
    client_id: int,
    client_data: ClientUpdateSchema,
    service: ClientService = Depends(get_service),
    user_data: UserData = Depends(get_current_user)
) -> ClientReadSchema:
    """Обновляет данные о клиенте."""
    if not user_data.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав для выполнения операции"
        )

    model = await service.update(
        query={"id": client_id},
        update_values=schema_model_dump(client_data),
    )
    return ClientReadSchema.model_validate(model)


@clients_router.delete(
    "/{client_id}",
    description='Удалить клиента',
    responses={
        status.HTTP_204_NO_CONTENT: {'description': 'Клиент успешно удален.'},
        status.HTTP_401_UNAUTHORIZED: {'model': Unauthorized},
    },
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_client(
    client_id: int,
    service: ClientService = Depends(get_service),
    user_data: UserData = Depends(get_current_user)
):
    if not user_data.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав для выполнения операции"
        )

    await service.delete(client_id=client_id)
