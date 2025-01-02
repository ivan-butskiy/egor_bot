import sqlalchemy as sa

from src.infrastructure.db.orm import mapper
from src.domain.suppliers.domain import Supplier


supplier = sa.Table(
    'supplier',
    mapper.metadata,
    sa.Column('tg_id', sa.Integer, primary_key=True),
    sa.Column('title', sa.String(255), nullable=False),
    sa.Column('alias', sa.String(255), nullable=False),
)


def start_mappers():
    mapper.map_imperatively(Supplier, supplier)
