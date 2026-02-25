from fastapi import APIRouter, Depends, HTTPException
from src.schemas.transactions import TransactionCreate, TransactionRead
from src.di.providers import get_create_transaction_uc, get_list_transactions_uc

router = APIRouter(prefix="/transactions", tags=["transactions"])

@router.post("/", response_model=TransactionRead)
async def create(data: TransactionCreate, uc=Depends(get_create_transaction_uc)):
    try:
        return await uc(
            transaction_type_id=data.transaction_type_id,
            amount=data.amount,
            date_=data.date,
            category_id=data.category_id,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[TransactionRead])
async def list_transactions(uc=Depends(get_list_transactions_uc)):
    return await uc()