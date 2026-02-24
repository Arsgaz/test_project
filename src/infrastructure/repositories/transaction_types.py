from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.db.schema import transaction_types


async def get_transaction_type_by_id(session: AsyncSession, type_id: int) -> dict | None:
    stmt = (
        select(
            transaction_types.c.id,
            transaction_types.c.code,
            transaction_types.c.name,
        )
        .where(transaction_types.c.id == type_id)
    )

    result = await session.execute(stmt)
    row = result.mappings().one_or_none()
    return dict(row) if row else None