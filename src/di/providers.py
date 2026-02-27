from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.db.deps import get_db_session

from src.infrastructure.repositories.transactions import TransactionsRepo
from src.infrastructure.repositories.categories import CategoriesRepo
from src.infrastructure.repositories.transaction_types import TransactionTypesRepo

from src.infrastructure.repositories.stats import StatsRepo
from src.application.services.stats import GetSummaryUseCase

from src.application.services.transactions import (
    CreateTransactionUseCase,
    ListTransactionsUseCase,
)
from src.application.services.categories import (
    CreateCategoryUseCase,
    ListCategoriesUseCase,
)

from src.infrastructure.db.uow import UnitOfWork
from src.infrastructure.db.session import SessionFactory


def get_uow() -> UnitOfWork:
    return UnitOfWork(SessionFactory)

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

def get_stats_repo(
    session: AsyncSession = Depends(get_db_session),
) -> StatsRepo:
    return StatsRepo(session)


# TRANSACTIONS USE CASES

def get_create_transaction_uc(
    uow: UnitOfWork = Depends(get_uow),
) -> CreateTransactionUseCase:
    return CreateTransactionUseCase(uow)


def get_list_transactions_uc(
    uow: UnitOfWork = Depends(get_uow),
) -> ListTransactionsUseCase:
    return ListTransactionsUseCase(uow)


#CATEGORIES USE CASES

def get_create_category_uc(
    uow: UnitOfWork = Depends(get_uow),
) -> CreateCategoryUseCase:
    return CreateCategoryUseCase(uow)


def get_list_categories_uc(
    uow: UnitOfWork = Depends(get_uow),
) -> ListCategoriesUseCase:
    return ListCategoriesUseCase(uow)

#STATS USE CASES 

def get_summary_uc(
    stats_repo: StatsRepo = Depends(get_stats_repo),
) -> GetSummaryUseCase:
    return GetSummaryUseCase(stats_repo)