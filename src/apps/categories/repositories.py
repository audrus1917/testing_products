"""Репозиторий приложения ``Пользователи``."""

from typing import Sequence, Any

from sqlalchemy import select
from sqlalchemy.orm import aliased
from sqlalchemy.engine import Row

from src.database.alchemy.repositories import AlchemyRepository
from src.apps.categories.models import Category


class CategoryRepository(AlchemyRepository):
    """Класс репозитория для работы с категориями."""

    model = Category

    async def get_tree(self, parent_id: int) -> Sequence[Row]:
        """Получение дерева категорий."""

        initial_query = select(self.model).where(
            self.model.id == parent_id
        ).cte(name="node_cte", recursive=True)

        node_alias = aliased(self.model, name="child")
        recursive_query = select(initial_query.union_all(
            select(node_alias).join(initial_query, node_alias.parent_id == initial_query.c.id)
        ))
        result = await self.session.execute(recursive_query)
        return result.all()


    async def get_ancestors(self, node_id: int) -> Sequence[Row]:
        """Получение списка предков для ноды."""
        initial_query = select(
            Category.id,
            Category.name,
            Category.parent_id
        ).where(
            Category.id == node_id
        ).cte(name="ancestors", recursive=True)
        recursive_query = select(
            Category.id,
            Category.name,
            Category.parent_id
        ).join(
            initial_query,
            initial_query.c.parent_id == Category.id
        )
        all_ancestors_cte = initial_query.union(
            recursive_query
        )
        result = await self.session.execute(
            select(Category).where(
                Category.id.in_(select(all_ancestors_cte.c.id))
            )
        )
        return result.all()
