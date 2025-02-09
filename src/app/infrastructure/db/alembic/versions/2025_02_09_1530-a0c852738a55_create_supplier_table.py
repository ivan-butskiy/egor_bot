"""create supplier table

Revision ID: a0c852738a55
Revises: 80b2917beb00
Create Date: 2025-02-09 15:30:18.095945

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a0c852738a55'
down_revision: Union[str, None] = '80b2917beb00'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'supplier',
        sa.Column('tg_id', sa.BigInteger, primary_key=True),
        sa.Column('title', sa.String(255), nullable=False, unique=True),
        sa.Column('alias', sa.String(255), nullable=False, unique=True),

        sa.PrimaryKeyConstraint('tg_id')
    )


def downgrade() -> None:
    op.drop_table('supplier')
