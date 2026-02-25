from fastapi import APIRouter, Depends, HTTPException

from src.application.services.transactions import (
    create_transaction_use_case,
    list_transactions_use_case,
)
from src.infrastructure.db.deps import get_transactions_repo
from src.infrastructure.repositories.transactions import TransactionsRepo
from src.schemas.transactions import TransactionCreate, TransactionRead


router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.post("/", response_model=TransactionRead)
async def create(
    data: TransactionCreate,
    transactions_repo: TransactionsRepo = Depends(get_transactions_repo),
):
    try:
        return await create_transaction_use_case(
            transactions_repo=transactions_repo,
            transaction_type_id=data.transaction_type_id,
            amount=data.amount,
            date_=data.date,
            category_id=data.category_id,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[TransactionRead])
async def list_transactions(
    transactions_repo: TransactionsRepo = Depends(get_transactions_repo),
):
    return await list_transactions_use_case(transactions_repo=transactions_repo)