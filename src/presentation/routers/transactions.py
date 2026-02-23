from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.db.deps import get_db_session
from src.infrastructure.repositories.categories import get_category_by_id
from src.infrastructure.repositories.transactions import create_transaction, get_transactions
from src.schemas.transactions import TransactionCreate, TransactionRead

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.post("/", response_model=TransactionRead)
async def create(data: TransactionCreate, session: AsyncSession = Depends(get_db_session)):
    category = await get_category_by_id(session, data.category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    if category["type"] != data.type.value:
        raise HTTPException(status_code=400, detail="Transaction type must match category type")

    return await create_transaction(
        session=session,
        type_=data.type.value,
        amount=data.amount,
        date_=data.date,
        category_id=data.category_id,
    )


@router.get("/", response_model=list[TransactionRead])
async def list_transactions(session: AsyncSession = Depends(get_db_session)):
    return await get_transactions(session)