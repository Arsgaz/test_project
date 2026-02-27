from pydantic import BaseModel, Field

class CategoryCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    transaction_type_id: int


class CategoryRead(BaseModel):
    id: int
    name: str
    transaction_type_id: int
    type: str  # "income" / "expense" из transaction_types.code