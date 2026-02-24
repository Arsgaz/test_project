from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession 

from src.infrastructure.db.deps import get_db_session
from src.application.services.stats import get_summary_use_case

router = APIRouter(prefix="/stats", tags = ["stats"])

@router.get("/summary")
async def summary(session: AsyncSession = Depends(get_db_session)): 
    return await get_summary_use_case(session)
