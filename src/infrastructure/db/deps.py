from fastapi import Depends
from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.db.session import SessionFactory
from src.infrastructure.repositories.transactions import TransactionsRepo

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionFactory() as session:
        yield session


def get_transactions_repo(
    session: AsyncSession = Depends(get_db_session),
) -> TransactionsRepo:
    return TransactionsRepo(session)