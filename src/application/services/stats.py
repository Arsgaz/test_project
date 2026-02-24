from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.repositories.stats import get_summary 

async def get_summary_use_case(session: AsyncSession) -> dict:
    return await get_summary(session)
 
