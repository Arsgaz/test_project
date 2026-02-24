from sqlalchemy import insert, select 
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.db.schema import transactions, transaction_types
async def create_transaction (
        session: AsyncSession, 
        transaction_type_id: int, 
        amount: float, 
        date_, 
        category_id: int 
) -> dict: 
    stmt = (
        insert(transactions)
        .values(type = transaction_type_id, amount = amount, date = date_, category_id = category_id)
        .returning (
            transactions.c.id,
            transactions.c.type,
            transactions.c.amount, 
            transactions.c.date, 
            transactions.c.category_id,
        )
    )
    result = await session.execute(stmt)
    await session.commit()
    return dict(result.mappings().one())
    
async def get_transactions(session: AsyncSession) -> list[dict]:
    stmt = (
        select(
            transactions.c.id,
            transaction_types.c.code.label("type"),
            transactions.c.amount,
            transactions.c.date,
            transactions.c.category_id,
        )
        .join(
            transaction_types,
            transactions.c.transaction_type_id == transaction_types.c.id,
        )
        .order_by(transactions.c.id.desc())
    )

    result = await session.execute(stmt)
    return [dict(r) for r in result.mappings().all()]
