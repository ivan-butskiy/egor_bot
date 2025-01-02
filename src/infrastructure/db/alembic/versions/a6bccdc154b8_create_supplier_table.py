"""create supplier table

Revision ID: a6bccdc154b8
Revises: ffbf1c4221ef
Create Date: 2024-12-23 20:48:27.584949

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a6bccdc154b8'
down_revision: Union[str, None] = 'ffbf1c4221ef'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'supplier',
        sa.Column('tg_id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String(255), nullable=False, unique=True),
        sa.Column('alias', sa.String(255), nullable=False, unique=True),

        sa.PrimaryKeyConstraint('tg_id')
    )


def downgrade() -> None:
    op.drop_table('supplier')
