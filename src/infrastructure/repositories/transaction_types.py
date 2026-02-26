from __future__ import annotations

from typing import Any
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.db.schema import transaction_types


class TransactionTypesRepo:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_id(self, type_id: int) -> dict[str, Any] | None:
        stmt = (
            select(
                transaction_types.c.id,
                transaction_types.c.code,
                transaction_types.c.name,
            )
            .where(transaction_types.c.id == type_id)
        )

        res = await self._session.execute(stmt)
        row = res.mappings().one_or_none()
        return dict(row) if row else None

    async def list(self) -> list[dict[str, Any]]:
        stmt = select(
            transaction_types.c.id,
            transaction_types.c.code,
            transaction_types.c.name,
        ).order_by(transaction_types.c.id.asc())

        res = await self._session.execute(stmt)
        return [dict(r) for r in res.mappings().all()]