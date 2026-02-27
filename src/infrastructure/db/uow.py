from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.infrastructure.repositories.categories import CategoriesRepo
from src.infrastructure.repositories.transactions import TransactionsRepo
from src.infrastructure.repositories.stats import StatsRepo
from src.infrastructure.repositories.transaction_types import TransactionTypesRepo


class UnitOfWork:
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        self._session_factory = session_factory
        self.session: AsyncSession | None = None

    async def __aenter__(self):
        self.session = self._session_factory()

        # создаём репозитории на одной сессии
        self.categories = CategoriesRepo(self.session)
        self.transactions = TransactionsRepo(self.session)
        self.transaction_types = TransactionTypesRepo(self.session)
        self.stats = StatsRepo(self.session)

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.session.rollback()
        else:
            await self.session.commit()

        await self.session.close()