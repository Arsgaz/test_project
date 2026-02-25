from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.db.schema import Categories


class CategoriesRepo:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, *, name: str, type_: str) -> dict:
        stmt = (
            insert(Categories)
            .values(name=name, type=type_)
            .returning(Categories.c.id, Categories.c.name, Categories.c.type)
        )
        res = await self._session.execute(stmt)
        await self._session.commit()
        return dict(res.mappings().one())

    async def list(self) -> list[dict]:
        stmt = select(Categories.c.id, Categories.c.name, Categories.c.type).order_by(Categories.c.id.desc())
        res = await self._session.execute(stmt)
        return [dict(r) for r in res.mappings().all()]

    async def get_by_id(self, category_id: int) -> dict | None:
        stmt = (
            select(Categories.c.id, Categories.c.name, Categories.c.type)
            .where(Categories.c.id == category_id)
        )
        res = await self._session.execute(stmt)
        row = res.mappings().one_or_none()
        return dict(row) if row else None