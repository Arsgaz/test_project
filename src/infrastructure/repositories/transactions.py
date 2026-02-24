from sqlalchemy import insert, select 
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.db.schema import transactions

async def create_transaction (
        session: AsyncSession, 
        type_: str, 
        amount: float, 
        date_, 
        category_id: int 
) -> dict: 
    stmt = (
        insert(transactions)
        .values(type = type_, amount = amount, date = date_, category_id = category_id)
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
    stmt = select(
        transactions.c.id,
            transactions.c.type,
            transactions.c.amount, 
            transactions.c.date, 
            transactions.c.category_id,
    ).order_by(transactions.c.id.desc())

    result = await session.execute(stmt)
    return [dict(r) for r in result.mappings().all()]
