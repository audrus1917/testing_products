"""Тесты для репозитория приложения ``Категории``."""

from typing import Optional

import pytest

from dataclasses import asdict

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

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
    """Тест каталога для репозитория `Категории``."""

    repository = CategoryRepository(
        session=session,
        model=Category
    )
    parent_entity = CategoryEntity(
        name="Родительская категория",
        description="Описание родительскрй категории"
    )
    parent_model: Optional[Category] = await repository.save(
        obj_data=asdict(parent_entity)
    )
    if parent_model is None:
        raise AssertionError("Ошибка при сохранении родительской категории")

    children: dict[int, list[int]] = {}
    parents: list[int] = [parent_model.id]
    for idx in range(1, 30):
        # Проверяем, что все "родители" уже заполнены
        current_parent = None
        for x in parents:
            x_children = children.setdefault(x, [])
            if len(x_children) < 3:
                current_parent = x
                break
        if current_parent is None:
            _parents = []
            for x in parents:
                _parents += children[x]
            parents = _parents
            current_parent = parents[0]

        children.setdefault(current_parent, [])

        new_entity = CategoryEntity(
            name=f"{idx}я категория",
            description=f"Описание {idx}й категории",
            parent_id=current_parent
        )
        new_model = await repository.save(obj_data=asdict(new_entity))
        children[current_parent].append(new_model.id)

    # Дерево
    categories_tree = await repository.get_tree(parent_id=parent_model.id)
    assert categories_tree is not None

    category_ancestors = await repository.get_ancestors(node_id=19)
    assert category_ancestors is not None
    ancestor_ids = [x[0].id for x in category_ancestors]
    assert 1 in ancestor_ids
    assert 2 in ancestor_ids
    assert 6 in ancestor_ids
