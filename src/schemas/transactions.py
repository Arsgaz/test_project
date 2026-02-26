from datetime import date 
from enum import Enum 
from typing import Literal

from pydantic import BaseModel, Field 

class TransactionType(str, Enum): 
    income = "income"
    expense = "expense"

class TransactionCreate(BaseModel):
    transaction_type_id: Literal[1, 2] = Field(
    ...,
    description="1 = income, 2 = expense"
    )
    amount: float = Field(gt=0)
    date: date 
    category_id: int 

class TransactionRead(BaseModel):
    id: int 
    type: TransactionType 
    amount: float 
    date: date 
    category_id: int 

