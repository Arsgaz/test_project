from sqlalchemy import insert, select 
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.db.schema import Categories


async def create_category(session: AsyncSession, name: str, type_: str) -> dict:
    stmt = (
        insert(Categories)
        .values(name=name, type=type_)
        .returning(Categories.c.id, Categories.c.name, Categories.c.type)
    )
    result = await session.execute(stmt)
    await session.commit()
    row = result.mappings().one()  # гарантированно не None, либо будет exception
    return dict(row)

async def get_categories(session: AsyncSession):
    stmt = select(Categories)
    result = await session.execute(stmt)
    return result.fetchall()
