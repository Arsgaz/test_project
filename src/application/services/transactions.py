async def create_transaction_use_case(
    *,
    transactions_repo,
    transaction_type_id: int,
    amount,
    date_,
    category_id: int,
) -> dict:
    if amount <= 0:
        raise ValueError("Amount must be greater than 0")

    return await transactions_repo.create(
        transaction_type_id=transaction_type_id,
        amount=amount,
        date_=date_,
        category_id=category_id,
    )


async def list_transactions_use_case(
    *,
    transactions_repo,
) -> list[dict]:
    return await transactions_repo.list()