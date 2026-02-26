from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.db.schema import Categories, transaction_types


class CategoriesRepo:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, *, name: str, transaction_type_id: int) -> dict:
        # 1) insert -> id
        insert_stmt = (
            insert(Categories)
            .values(name=name, transaction_type_id=transaction_type_id)
            .returning(Categories.c.id)
        )
        res = await self._session.execute(insert_stmt)
        new_id = res.scalar_one()
        await self._session.commit()

        # 2) select + join -> красивый ответ
        select_stmt = (
            select(
                Categories.c.id,
                Categories.c.name,
                Categories.c.transaction_type_id,
                transaction_types.c.code.label("type"),
            )
            .select_from(
                Categories.join(
                    transaction_types,
                    Categories.c.transaction_type_id == transaction_types.c.id,
                )
            )
            .where(Categories.c.id == new_id)
        )
        res = await self._session.execute(select_stmt)
        return dict(res.mappings().one())

    async def list(self) -> list[dict]:
        stmt = (
            select(
                Categories.c.id,
                Categories.c.name,
                Categories.c.transaction_type_id,
                transaction_types.c.code.label("type"),
            )
            .select_from(
                Categories.join(
                    transaction_types,
                    Categories.c.transaction_type_id == transaction_types.c.id,
                )
            )
            .order_by(Categories.c.id.desc())
        )
        res = await self._session.execute(stmt)
        return [dict(r) for r in res.mappings().all()]

    async def get_by_id(self, category_id: int) -> dict | None:
        stmt = (
            select(
                Categories.c.id,
                Categories.c.name,
                Categories.c.transaction_type_id,
                transaction_types.c.code.label("type"),
            )
            .select_from(
                Categories.join(
                    transaction_types,
                    Categories.c.transaction_type_id == transaction_types.c.id,
                )
            )
            .where(Categories.c.id == category_id)
        )
        res = await self._session.execute(stmt)
        row = res.mappings().one_or_none()
        return dict(row) if row else None