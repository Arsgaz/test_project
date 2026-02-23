from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.db.deps import get_db_session
from src.infrastructure.repositories.categories import (
    create_category,
    get_categories,
)
from src.schemas.categories import CategoryCreate, CategoryRead

router = APIRouter(prefix="/categories", tags=["categories"])


@router.post("/", response_model=CategoryRead)
async def create(data: CategoryCreate, session: AsyncSession = Depends(get_db_session)):
    return await create_category(session, data.name, data.type)


@router.get("/", response_model=list[CategoryRead])
async def list_categories(session: AsyncSession = Depends(get_db_session)):
    return await get_categories(session)