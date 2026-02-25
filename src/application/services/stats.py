class GetSummaryUseCase:
    def __init__(self, stats_repo):
        self._stats = stats_repo

    async def __call__(self) -> dict:
        return await self._stats.get_summary()
