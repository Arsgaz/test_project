from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.db.deps import get_db_session

from src.infrastructure.repositories.transactions import TransactionsRepo
from src.infrastructure.repositories.categories import CategoriesRepo
from src.infrastructure.repositories.transaction_types import TransactionTypesRepo

from src.application.services.transactions import (
    CreateTransactionUseCase,
    ListTransactionsUseCase,
)
from src.application.services.categories import (
    CreateCategoryUseCase,
    ListCategoriesUseCase,
)


#REPOS

def get_transactions_repo(
    session: AsyncSession = Depends(get_db_session),
) -> TransactionsRepo:
    return TransactionsRepo(session)


def get_categories_repo(
    session: AsyncSession = Depends(get_db_session),
) -> CategoriesRepo:
    return CategoriesRepo(session)


def get_transaction_types_repo(
    session: AsyncSession = Depends(get_db_session),
) -> TransactionTypesRepo:
    return TransactionTypesRepo(session)


# TRANSACTIONS USE CASES

def get_create_transaction_uc(
    transactions_repo: TransactionsRepo = Depends(get_transactions_repo),
    categories_repo: CategoriesRepo = Depends(get_categories_repo),
    transaction_types_repo: TransactionTypesRepo = Depends(get_transaction_types_repo),
) -> CreateTransactionUseCase:
    return CreateTransactionUseCase(transactions_repo, categories_repo, transaction_types_repo)


def get_list_transactions_uc(
    transactions_repo: TransactionsRepo = Depends(get_transactions_repo),
) -> ListTransactionsUseCase:
    return ListTransactionsUseCase(transactions_repo)


#CATEGORIES USE CASES

def get_create_category_uc(
    categories_repo: CategoriesRepo = Depends(get_categories_repo),
    transaction_types_repo: TransactionTypesRepo = Depends(get_transaction_types_repo),
) -> CreateCategoryUseCase:
    return CreateCategoryUseCase(categories_repo, transaction_types_repo)


def get_list_categories_uc(
    categories_repo: CategoriesRepo = Depends(get_categories_repo),
) -> ListCategoriesUseCase:
    return ListCategoriesUseCase(categories_repo)