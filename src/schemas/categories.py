from pydantic import BaseModel 
from enum import Enum

class CategoryType (str, Enum):
    income = "income"
    expense = "expense"

class CategoryCreate(BaseModel):
    name: str
    type: CategoryType

class CategoryRead(BaseModel):
    id: int 
    name: str 
    type: CategoryType
    
