"""Тесты для репозитория приложения ``Категории``."""

import math

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
    parent_model = await repository.save(obj_data=asdict(parent_entity))

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

    initial_query = select(Category).where(
        Category.id == parent_model.id
    ).cte(name="node_cte", recursive=True)

    node_alias = aliased(Category, name="child")
    recursive_query = select(initial_query.union_all(
        select(node_alias).join(initial_query, node_alias.parent_id == initial_query.c.id)
    ))
    result = await session.execute(recursive_query)
    for row in result.all():
        print(row.id, row.parent_id, row.name)