from sqlalchemy import insert, select 
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.db.schema import transcaction 

async def create_transaction (
        session: AsyncSession, 
        type_: str, 
        amount: float, 
        date_, 
        category_id: int 
) -> dict: 
    stmt = (
        insert(transcaction)
        .values(type = type_, amount = amount, date = date_, category_id = category_id)
        .returning (
            transcaction.c.id,
            transcaction.c.type,
            transcaction.c.amount, 
            transcaction.c.date, 
            transcaction.c.category_id,
        )
    )
    result = await session.execute(stmt)
    await session.commit()
    return dict(result.mappings().one())
    
async def get_transactions(session: AsyncSession) -> list[dict]:
    stmt = select(
        transcaction.c.id,
            transcaction.c.type,
            transcaction.c.amount, 
            transcaction.c.date, 
            transcaction.c.category_id,
    ).order_by(transcaction.c.id.desc())

    result = await session.execute(stmt)
    return [dict(r) for r in result.mappings().all()]
