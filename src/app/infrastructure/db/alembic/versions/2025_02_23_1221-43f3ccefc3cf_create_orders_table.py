"""create orders table

Revision ID: 43f3ccefc3cf
Revises: a0c852738a55
Create Date: 2025-02-23 12:21:18.901464

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '43f3ccefc3cf'
down_revision: Union[str, None] = 'a0c852738a55'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'orders',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('supplier_tg_id', sa.BigInteger),
        sa.Column('user_tg_id', sa.BigInteger),
        sa.Column('message_id', sa.BigInteger, nullable=False),
        sa.Column('text', sa.Text, nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False),

        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['supplier_tg_id'], ['supplier.tg_id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['user_tg_id'], ['user.tg_id'], ondelete='SET NULL')
    )

    op.create_index(op.f('ix_orders_supplier_tg_id'), 'orders', ['supplier_tg_id'])
    op.create_index(op.f('ix_orders_user_tg_id'), 'orders', ['user_tg_id'])


def downgrade() -> None:
    op.drop_table('orders')
