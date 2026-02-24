from datetime import date 
from enum import Enum 

from pydantic import BaseModel, Field 

class TransactionType(str, Enum): 
    income = "income"
    expense = "expense"

class TransactionCreate(BaseModel):
    type: TransactionType
    amount: float = Field(gt=0)
    date: date 
    category_id: int 

class TransactionRead(BaseModel):
    id: int 
    type: TransactionType 
    amount: float 
    date: date 
    category_id: int 

