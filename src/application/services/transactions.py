from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.repositories.categories import get_category_by_id
from src.infrastructure.repositories.transactions import create_transaction


async def create_transaction_use_case(
    session: AsyncSession,
    type_: str,
    amount: float,
    date_,
    category_id: int,
) -> dict:
    category = await get_category_by_id(session, category_id)

    if category is None:
        raise ValueError("Category not found")

    if category["type"] != type_:
        raise ValueError("Transaction type must match category type")

    return await create_transaction(
        session=session,
        type_=type_,
        amount=amount,
        date_=date_,
        category_id=category_id,
    )