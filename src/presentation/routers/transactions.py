from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.db.deps import get_db_session
from src.application.services.transactions import create_transaction_use_case
from src.infrastructure.repositories.transactions import get_transactions
from src.schemas.transactions import TransactionCreate, TransactionRead

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.post("/", response_model=TransactionRead)
async def create(data: TransactionCreate, session: AsyncSession = Depends(get_db_session)):
    try:
        return await create_transaction_use_case(
            session=session,
            transaction_type_id=data.transaction_type_id,
            amount=data.amount,
            date_=data.date,
            category_id=data.category_id,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[TransactionRead])
async def list_transactions(session: AsyncSession = Depends(get_db_session)):
    return await get_transactions(session)