from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.db.schema import transactions, transaction_types


class TransactionsRepo:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(
        self,
        *,
        transaction_type_id: int,
        amount,
        date_,
        category_id: int,
    ) -> dict:

        insert_stmt = (
            insert(transactions)
            .values(
                transaction_type_id=transaction_type_id,
                amount=amount,
                date=date_,
                category_id=category_id,
            )
            .returning(transactions.c.id)
        )

        res = await self._session.execute(insert_stmt)
        new_id = res.scalar_one()

        # вместо commit
        await self._session.flush()

        select_stmt = (
            select(
                transactions.c.id,
                transaction_types.c.code.label("type"),
                transactions.c.amount,
                transactions.c.date,
                transactions.c.category_id,
            )
            .select_from(
                transactions.join(
                    transaction_types,
                    transactions.c.transaction_type_id == transaction_types.c.id,
                )
            )
            .where(transactions.c.id == new_id)
        )

        res = await self._session.execute(select_stmt)
        return dict(res.mappings().one())

    async def list(self) -> list[dict]:
        stmt = (
            select(
                transactions.c.id,
                transaction_types.c.code.label("type"),
                transactions.c.amount,
                transactions.c.date,
                transactions.c.category_id,
            )
            .select_from(
                transactions.join(
                    transaction_types,
                    transactions.c.transaction_type_id == transaction_types.c.id,
                )
            )
            .order_by(transactions.c.id.desc())
        )

        result = await self._session.execute(stmt)
        return [dict(r) for r in result.mappings().all()]