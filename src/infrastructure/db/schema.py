import enum 
from sqlalchemy import (MetaData, 
    Table, 
    Column, 
    Integer,
    String,
    Date,
    DateTime, 
    Numeric,
    ForeignKey, 
    Enum, 
    func, 
    )

metadata = MetaData()

class CategoryType(str, enum.Enum):
    income = "income"
    expense = "expense"

class TransactionType(str, enum.Enum):
    income = "income"
    expense = "expense"

Categories = Table (
    "categories",
    metadata,
    Column("id", Integer, primary_key = True),
    Column("name", String(100), nullable = False),
    Column("type", Enum(CategoryType, name = "category_type"), nullable = False),
    Column("created_at", DateTime(timezone = True), server_default=func.now(), nullable = False)
)

transactions = Table(
    "transactions", 
    metadata, 
    Column("id", Integer, primary_key=True),
    Column("type", Enum(TransactionType, name = "transaction_type")),
    Column("amount", Numeric(12, 2), nullable = False),
    Column("date", Date, nullable = False),
    Column("category_id", Integer, ForeignKey("categories.id", ondelete = "RESTRICT"), nullable = False),
    Column("created_at", DateTime(timezone = True), server_default=func.now(), nullable = False)
)