from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.repositories.categories import get_category_by_id
from src.infrastructure.repositories.transaction_types import get_transaction_type_by_id
from src.infrastructure.repositories.transactions import create_transaction


async def create_transaction_use_case(
    session: AsyncSession,
    transaction_type_id: int,
    amount: float,
    date_,
    category_id: int,
) -> dict:
    category = await get_category_by_id(session, category_id)
    if category is None:
        raise ValueError("Category not found")

    tx_type = await get_transaction_type_by_id(session, transaction_type_id)
    if tx_type is None:
        raise ValueError("Transaction type not found")

    
    if category["transaction_type_id"] != transaction_type_id:
        raise ValueError("Transaction type must match category type")

    return await create_transaction(
        session=session,
        transaction_type_id=transaction_type_id,
        amount=amount,
        date_=date_,
        category_id=category_id,
    )