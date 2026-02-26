from fastapi import APIRouter, Depends

from src.di.providers import get_summary_uc

router = APIRouter(prefix="/stats", tags=["stats"])


@router.get("/summary")
async def summary(uc=Depends(get_summary_uc)):
    return await uc()