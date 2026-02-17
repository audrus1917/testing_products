"""Тесты для репозитория приложения ``Категории``."""

import pytest

from dataclasses import asdict

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.categories.entities import CategoryEntity
from src.apps.categories.models import Category
from src.apps.categories.repositories import CategoryRepository


@pytest.mark.anyio
async def test_save(session: AsyncSession):
    """Тест добавления для репозитория `Категории``."""

    repository = CategoryRepository(
        session=session,
        model=Category
    )

    new_entity = CategoryEntity(
        name="Первая категория",
        description="Описание категории"
    )

    new_model = await repository.save(obj_data=asdict(new_entity))
    assert new_model is not None

    base_stmt = select(Category)

    sample_model = await repository.get(
        base_stmt.where(Category.id == new_model.id)
    )
    assert sample_model is not None


@pytest.mark.anyio
async def test_build_tree(session: AsyncSession):
    """Тест добавления для репозитория `Категории``."""

    repository = CategoryRepository(
        session=session,
        model=Category
    )

    new_entity = CategoryEntity(
        name="Первая категория",
        description="Описание категории"
    )

    new_model = await repository.save(obj_data=asdict(new_entity))
    assert new_model is not None

    base_stmt = select(Category)

    sample_model = await repository.get(
        base_stmt.where(Category.id == new_model.id)
    )
    assert sample_model is not None
