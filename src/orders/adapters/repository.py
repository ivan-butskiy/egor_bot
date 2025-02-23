import abc
from typing import Set, List

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.adapters.repository import BaseAbstractRepository
from src.orders import Order


class AbstractRepository(BaseAbstractRepository, abc.ABC):
    seen: Set[Order]


class SQLAlchemyRepository(AbstractRepository):

    def __init__(self, session: AsyncSession):
        super().__init__()
        self.session = session

    async def _add(self, order: Order) -> None:
        self.seen.add(order)
        self.session.add(order)

    async def _get(self, id_: int, *args, **kwargs) -> Order:
        stmt = sa.select(Order).where(Order.id == id_)
        res = await self.session.execute(stmt)
        return res.scalar()

    async def _delete(self, id_: int) -> None:
        stmt = sa.delete(Order).where(Order.id == id_)
        await self.session.execute(stmt)

    async def _get_list(self, limit: int, offset: int) -> List[Order]:
        res = await (
            self.session.execute(
                sa.select(Order)
                .order_by(sa.desc(Order.created_at))
                .limit(limit)
                .offset(offset)
            )
        )

        return list(res.scalars())

    async def _count(self) -> int:
        stmt = (
            sa.select(sa.func.count(1))
            .select_from(Order)
        )

        res = await self.session.execute(stmt)
        return res.scalar()

    async def _exists(self) -> bool:
        raise NotImplementedError
