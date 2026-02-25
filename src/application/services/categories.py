class CreateCategoryUseCase:
    def __init__(self, categories_repo):
        self._categories = categories_repo

    async def __call__(self, *, name: str, type_: str) -> dict:
        name = name.strip()
        if not name:
            raise ValueError("Name is required")

        # минимальная бизнес-валидация
        if type_ not in ("income", "expense"):
            raise ValueError("Invalid category type")

        return await self._categories.create(
            name=name,
            type_=type_,
        )


class ListCategoriesUseCase:
    def __init__(self, categories_repo):
        self._categories = categories_repo

    async def __call__(self) -> list[dict]:
        return await self._categories.list()