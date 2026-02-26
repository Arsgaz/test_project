class CreateCategoryUseCase:
    def __init__(self, categories_repo, transaction_types_repo):
        self._categories = categories_repo
        self._types = transaction_types_repo

    async def __call__(self, *, name: str, transaction_type_id: int) -> dict:
        name = name.strip()
        if not name:
            raise ValueError("Name is required")

        # бизнес-валидация: тип должен существовать (чтобы не ловить 500 от FK)
        tx_type = await self._types.get_by_id(transaction_type_id)
        if tx_type is None:
            raise ValueError("Transaction type not found")

        return await self._categories.create(
            name=name,
            transaction_type_id=transaction_type_id,
        )


class ListCategoriesUseCase:
    def __init__(self, categories_repo):
        self._categories = categories_repo

    async def __call__(self) -> list[dict]:
        return await self._categories.list()