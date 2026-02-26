"""Tests for SQLAlchemy base repoisitory."""

import pytest

from sqlalchemy import Integer, String, Identity, select, func
from sqlalchemy.orm import Mapped, mapped_column

from src.database.alchemy import Base
from database.alchemy.repositories import AlchemyRepository
from src.core.database.exceptions import InvalidQueryError

@pytest.mark.anyio
async def test_repository(engine, session):
    """Tests for the :cls:`AlchemyRepository`."""

    class A(Base):
        """Testing model."""

        __tablename__ = "a"

        id: Mapped[int] = mapped_column(Integer, Identity(), primary_key=True)
        code: Mapped[str] = mapped_column(String(10), unique=True)
        name: Mapped[str] = mapped_column(String(50), index=True)

        def __repr__(self):
            return f"{self.name} (ID={self.id})"

    a_repository = AlchemyRepository(
        session=session,
        model=A
    )

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.tables["a"].create)

    to_add = [A(code=f"c{idx}", name=f"sample_{idx}") for idx in range(25)]

    session.add_all(to_add)
    await session.flush()
    await session.commit()

    not_uniq_code = A(code="c1", name="sample_test")
    with pytest.raises(InvalidQueryError):
        await a_repository.save(obj=not_uniq_code)
        await session.commit()
    await session.rollback()

    base_stmt = select(A)

    sample_1 = await a_repository.get(base_stmt.where(A.name == "sample_1"))
    assert sample_1 is not None
    assert isinstance(sample_1, A)
    sample_1_id = sample_1.id

    await a_repository.update(
        query=base_stmt.filter(A.name == "sample_1"),
        update_values={A.name: "Test"}
    )
    await session.refresh(sample_1)
    assert sample_1.name == "Test"
    await session.commit()

    sample_2 = await a_repository.get(base_stmt.where(A.name == "sample_2"))
    sample_2.name = "Sample 2 - test"
    assert a_repository.is_modified(sample_2) is True
    await session.rollback()

    result = await a_repository.filter(
        base_stmt.filter(A.name.regexp_match(r".*?2$"))
    )
    assert len(result) == 3

    await a_repository.delete(sample_1)
    await session.commit()

    sample_1 = await a_repository.get(base_stmt.where(A.id == sample_1_id))
    assert sample_1 is None
