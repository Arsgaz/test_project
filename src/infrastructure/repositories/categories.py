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
    row = result.mappings().one()  
    return dict(row)

async def get_categories(session: AsyncSession):
    stmt = select(Categories)
    result = await session.execute(stmt)
    return result.fetchall()

async def get_category_by_id(session: AsyncSession, category_id: int) -> dict | None:
    stmt = select (
        Categories.c.id, 
        Categories.c.name, 
        Categories.c.type, 
    ).where(Categories.c.id == category_id)

    result = await session.execute(stmt)
    row = result.mappings().one_or_none()
    return dict(row) if row else None 
