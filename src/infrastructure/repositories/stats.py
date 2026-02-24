from sqlalchemy import select, func, case 
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.db.schema import transactions 

async def get_summary(session:AsyncSession) -> dict: 
    stmt = select (
        func.coalesce(
            func.sum(case((transactions.c.type == "income", transactions.c.amount), else_ = 0)), 0
        ).label("total_income"),
        func.coalesce(
            func.sum(case((transactions.c.type == "expense", transactions.c.amount), else_ = 0)), 0
        ).label("total_expense"),
    )
    result = await session.execute(stmt)
    row = result.mappings().one()
    total_income = float(row["total_income"])
    total_expense = float(row["total_expense"])
    return {
        "total_income": total_income, 
        "total_expense": total_expense, 
        "balance": total_income - total_expense
    }
  