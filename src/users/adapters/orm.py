import sqlalchemy as sa

from src.app.infrastructure.db.orm import mapper
from src.users.domain import User, UserTypeEnum


user = sa.Table(
    'user',
    mapper.metadata,
    sa.Column('tg_id', sa.BigInteger, primary_key=True),
    sa.Column('first_name', sa.String(length=256), nullable=False),
    sa.Column('last_name', sa.String(length=256), nullable=False),
    sa.Column('type', sa.Enum(UserTypeEnum), nullable=False)
)


def start_mappers():
    mapper.map_imperatively(User, user)
