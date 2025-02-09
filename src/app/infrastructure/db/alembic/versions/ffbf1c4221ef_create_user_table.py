"""create user table

Revision ID: ffbf1c4221ef
Revises: 
Create Date: 2024-12-15 12:59:20.600065

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from src.users.domain.model import UserTypeEnum


# revision identifiers, used by Alembic.
revision: str = 'ffbf1c4221ef'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'user',
        sa.Column('tg_id', sa.Integer, primary_key=True),
        sa.Column('user_name', sa.String(length=256), nullable=False),
        sa.Column('first_name', sa.String(length=256), nullable=False),
        sa.Column('last_name', sa.String(length=256)),
        sa.Column('type', sa.Enum(UserTypeEnum), nullable=False),

        sa.PrimaryKeyConstraint('tg_id')
    )


def downgrade() -> None:
    op.drop_table('user')
    op.execute("DROP TYPE IF EXISTS usertypeenum;")
