from sqlalchemy import select, func, case
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.db.schema import transactions, transaction_types


class StatsRepo:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_summary(self) -> dict:
        stmt = (
            select(
                func.coalesce(
                    func.sum(
                        case(
                            (transaction_types.c.code == "income", transactions.c.amount),
                            else_=0,
                        )
                    ),
                    0,
                ).label("total_income"),
                func.coalesce(
                    func.sum(
                        case(
                            (transaction_types.c.code == "expense", transactions.c.amount),
                            else_=0,
                        )
                    ),
                    0,
                ).label("total_expense"),
            )
            .select_from(
                transactions.join(
                    transaction_types,
                    transactions.c.transaction_type_id == transaction_types.c.id,
                )
            )
        )

        result = await self._session.execute(stmt)
        row = result.mappings().one()

        total_income = float(row["total_income"])
        total_expense = float(row["total_expense"])

        return {
            "total_income": total_income,
            "total_expense": total_expense,
            "balance": total_income - total_expense,
        }