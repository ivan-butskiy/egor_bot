import sqlalchemy as sa
from sqlalchemy.orm import relationship

from src.app.infrastructure.db.orm import mapper
from src.orders import Order


order = sa.Table(
    'orders',
    mapper.metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('supplier_tg_id', sa.BigInteger, sa.ForeignKey('supplier.tg_id', ondelete='SET NULL')),
    sa.Column('user_tg_id', sa.BigInteger, sa.ForeignKey('user.tg_id', ondelete='SET NULL')),
    sa.Column('message_id', sa.BigInteger, nullable=False),
    sa.Column('text', sa.Text, nullable=False),
    sa.Column('created_at', sa.DateTime, nullable=False),
)


def start_mappers():
    mapper.map_imperatively(
        Order,
        order,
        properties={
            'supplier': relationship(
                'Supplier', lazy='joined',
                primaryjoin='Order.supplier_tg_id==Supplier.tg_id'
            ),
            'user': relationship(
                'User', lazy='joined',
                primaryjoin='Order.user_tg_id==User.tg_id'
            )
        }
    )
