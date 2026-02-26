"""categories: type -> transaction_type_id

Revision ID: 9d0aec281824
Revises: 717fe6440139
Create Date: 2026-02-26 16:21:36.417682

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9d0aec281824'
down_revision: Union[str, Sequence[str], None] = '717fe6440139'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1) добавляем новую колонку (временно nullable)
    op.add_column(
        "categories",
        sa.Column("transaction_type_id", sa.Integer(), nullable=True),
    )

    # 2) переносим данные из старого enum type -> transaction_types.id
    # предполагаем, что transaction_types уже содержит income/expense с id 1/2
    op.execute("""
        UPDATE categories
        SET transaction_type_id = CASE
            WHEN type = 'income' THEN 1
            WHEN type = 'expense' THEN 2
            ELSE NULL
        END
    """)

    # 3) ставим NOT NULL (если хочешь строго)
    # если в categories могут быть строки с NULL type/невалидные — оставь nullable=True
    op.alter_column("categories", "transaction_type_id", nullable=False)

    # 4) создаём FK
    op.create_foreign_key(
        "fk_categories_transaction_type_id",
        "categories",
        "transaction_types",
        ["transaction_type_id"],
        ["id"],
        ondelete="RESTRICT",
    )

    # 5) удаляем старую колонку type
    op.drop_column("categories", "type")


def downgrade() -> None:
    # 1) возвращаем колонку type (enum)
    category_type = sa.Enum("income", "expense", name="category_type")
    category_type.create(op.get_bind(), checkfirst=True)

    op.add_column("categories", sa.Column("type", category_type, nullable=True))

    # 2) переносим обратно transaction_type_id -> type (через join)
    op.execute("""
        UPDATE categories c
        SET type = tt.code
        FROM transaction_types tt
        WHERE c.transaction_type_id = tt.id
    """)

    # 3) убираем FK и колонку transaction_type_id
    op.drop_constraint("fk_categories_transaction_type_id", "categories", type_="foreignkey")
    op.drop_column("categories", "transaction_type_id")