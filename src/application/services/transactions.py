from datetime import date
from decimal import Decimal

class CreateTransactionUseCase:
    def __init__(self, transactions_repo, categories_repo, transaction_types_repo):
        self._transactions = transactions_repo
        self._categories = categories_repo
        self._types = transaction_types_repo

    async def __call__(
        self,
        *,
        transaction_type_id: int,
        amount: Decimal,
        date_: date,
        category_id: int,
    ) -> dict:
        tx_type = await self._types.get_by_id(transaction_type_id)
        if tx_type is None:
            raise ValueError("Transaction type not found")

        category = await self._categories.get_by_id(category_id)
        if category is None:
            raise ValueError("Category not found")

        if category["type"] != tx_type["code"]:
            raise ValueError("Transaction type must match category type")

        return await self._transactions.create(
            transaction_type_id=transaction_type_id,
            amount=amount,
            date_=date_,
            category_id=category_id,
        )


class ListTransactionsUseCase:
    def __init__(self, transactions_repo):
        self._transactions = transactions_repo

    async def __call__(self) -> list[dict]:
        return await self._transactions.list()