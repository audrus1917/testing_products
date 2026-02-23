from __future__ import annotations

from typing import Optional

import logging

from pydantic import ValidationError

from fastapi.exceptions import HTTPException
from fastapi import APIRouter, status, Depends, Form
from fastapi_cache.decorator import cache

from src.core.http_response_schemas import UniqueConstraint, Unauthorized
from src.core.exceptions import UniqueConstraintError

from src.oauth2.tokens import get_current_user
from src.oauth2.passwords import get_password_hash
from src.apps.api_error_wrapper import api_error_wrapper
from src.apps.users.models import User
from src.apps.users.schemas import (
    UserCreateSchema,
    UserReadSchema,
    UserUpdateSchema
)
from src.apps.users.services import UserService
from src.apps.users.depends import get_service


logger = logging.getLogger(__name__)

users_router = APIRouter(
    tags=["users"]
)


@users_router.post(
    "/",
    response_model=UserReadSchema,
    responses={
        status.HTTP_201_CREATED: {'model': UserReadSchema},
        status.HTTP_400_BAD_REQUEST: {'model': UniqueConstraint},
    },
    description="Создание нового пользователя",
    status_code=status.HTTP_201_CREATED,
)
@api_error_wrapper.decorate
async def create(
    user_data: UserCreateSchema,
    service: UserService = Depends(get_service),
) -> UserReadSchema:
    
    to_create = user_data.model_dump()
    password = to_create.pop("password")
    to_create["hashed_password"] = get_password_hash(password)
    
    try:
        result = await service.create(obj_data=to_create)
        return UserReadSchema.model_validate(result)
    except UniqueConstraintError as exc:
        raise HTTPException(
            detail=f'Пользователь с почтой <{user_data.email}> уже зарегистрирован в системе',
            status_code=status.HTTP_400_BAD_REQUEST,
        ) from exc

    except ValidationError as exc:
        raise HTTPException(
            detail=f'Ошибка валидации: {exc}',
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        ) from exc


# @users_router.delete(
#     '',
#     description='Удалить пользователя',
#     responses={
#         status.HTTP_204_NO_CONTENT: {'description': 'Пользователь успешно удален.'},
#         status.HTTP_401_UNAUTHORIZED: {'model': Unauthorized},
#     },
#     status_code=status.HTTP_204_NO_CONTENT,
# )
# async def user_delete(
#     service: UserService = Depends(get_service),
#     user: UserModel = Depends(get_current_user),
# ):
#     await service.delete(user_pk=user.id)


# @users_router.patch(
#     '',
#     description='Частично обновить учетные данные пользователя',
#     status_code=status.HTTP_200_OK,
#     responses={
#         status.HTTP_200_OK: {'model': UserUpdateSchema},
#         status.HTTP_401_UNAUTHORIZED: {'model': Unauthorized},
#         status.HTTP_400_BAD_REQUEST: {'model': UniqueConstraint},
#     },
#     response_model=UserOutSchema,
# )
# async def user_edit(
#     user_to_update: UserUpdateSchema,
#     controller: UserController = Depends(get_controller),
#     user: UserModel = Depends(get_current_user),
# ) -> UserOutSchema:
#     """Updates and returns the :cls:`User`."""
#     try:
#         return await controller.update(data=user_to_update, user_pk=user.id)
#     except UserAlreadyExists as exc:
#         raise UniqueConstraintError(
#             detail=f'Пользователь с почтой <{user_to_update.email}> уже зарегистрирован в системе',
#             status_code=status.HTTP_400_BAD_REQUEST,
#         ) from exc


# @users_router.get(
#     '/me',
#     description='Получение информации о текущем пользователе.',
#     status_code=status.HTTP_200_OK,
#     responses={
#         status.HTTP_401_UNAUTHORIZED: {'model': Unauthorized},
#         status.HTTP_200_OK: {'model': UserOutSchema},
#     },
#     response_model=UserOutSchema,
# )
# @cache(expire=60 * 60)
# async def get_user(
#     controller: UserController = Depends(get_controller),
#     user: UserModel = Depends(get_current_user),
# ) -> UserOutSchema:
#     return await controller.get_by_pk(user_pk=user.id)
