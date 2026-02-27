class CreateCategoryUseCase:
    def __init__(self, uow):
        self._uow = uow

    async def __call__(self, *, name: str, transaction_type_id: int) -> dict:
        name = name.strip()
        if not name:
            raise ValueError("Name is required")

        async with self._uow as uow:
            # бизнес-валидация: тип должен существовать
            tx_type = await uow.transaction_types.get_by_id(transaction_type_id)
            if tx_type is None:
                raise ValueError("Transaction type not found")

            return await uow.categories.create(
                name=name,
                transaction_type_id=transaction_type_id,
            )


class ListCategoriesUseCase:
    def __init__(self, uow):
        self._uow = uow

    async def __call__(self) -> list[dict]:
        async with self._uow as uow:
            return await uow.categories.list()