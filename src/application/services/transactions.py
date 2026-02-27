from datetime import date
from decimal import Decimal

class CreateTransactionUseCase:
    def __init__(self, uow):
        self._uow = uow

    async def __call__(
        self,
        *,
        transaction_type_id: int,
        amount: Decimal,
        date_: date,
        category_id: int,
    ) -> dict:

        async with self._uow as uow:
            tx_type = await uow.transaction_types.get_by_id(transaction_type_id)
            if tx_type is None:
                raise ValueError("Transaction type not found")

            category = await uow.categories.get_by_id(category_id)
            if category is None:
                raise ValueError("Category not found")

            if category["type"] != tx_type["code"]:
                raise ValueError("Transaction type must match category type")

            return await uow.transactions.create(
                transaction_type_id=transaction_type_id,
                amount=amount,
                date_=date_,
                category_id=category_id,
            )


class ListTransactionsUseCase:
    def __init__(self, uow):
        self._uow = uow

    async def __call__(self) -> list[dict]:
        async with self._uow as uow:
            return await uow.transactions.list()