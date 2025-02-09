import sqlalchemy as sa

from src.app.infrastructure.db.orm import mapper
from src.suppliers.domain import Supplier


supplier = sa.Table(
    'supplier',
    mapper.metadata,
    sa.Column('tg_id', sa.BigInteger, primary_key=True),
    sa.Column('title', sa.String(255), nullable=False),
    sa.Column('alias', sa.String(255), nullable=False),
)


def start_mappers():
    mapper.map_imperatively(Supplier, supplier)
