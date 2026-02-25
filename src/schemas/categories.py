from pydantic import BaseModel, Field
from enum import Enum


class CategoryType (str, Enum):
    income = "income"
    expense = "expense"

class CategoryCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    type: CategoryType


class CategoryRead(BaseModel):
    id: int
    name: str
    type: CategoryType
