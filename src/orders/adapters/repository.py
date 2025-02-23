import abc
from typing import Set, List, Self, Any

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.adapters.repository import BaseAbstractRepository
from src.orders import Order


class AbstractRepository(BaseAbstractRepository, abc.ABC):
    seen: Set[Order]

    def related_to_user_tg_id(self, user_tg_id: int) -> Self:
        return self._related_to_user_tg_id(user_tg_id)

    def related_to_supplier_tg_id(self, supplier_tg_id: int) -> Self:
        return self._related_to_supplier_tg_id(supplier_tg_id)

    def reset_stmt(self) -> None:
        self._reset_stmt()

    async def get_list(self, limit: int, offset: int, reset_stmt: bool = True, *args, **kwargs) -> List[Any]:
        return await super().get_list(limit, offset, reset_stmt, *args, **kwargs)

    @abc.abstractmethod
    async def _get_list(self, limit: int, offset: int, *args, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def _related_to_user_tg_id(self, user_tg_id: int) -> Self:
        raise NotImplementedError

    @abc.abstractmethod
    def _related_to_supplier_tg_id(self, supplier_tg_id: int) -> Self:
        raise NotImplementedError

    @abc.abstractmethod
    def _reset_stmt(self) -> None:
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):

    _stmt = sa.Select

    def __init__(self, session: AsyncSession):
        super().__init__()
        self.session = session
        self._reset_stmt()

    def _reset_stmt(self) -> None:
        self._stmt = sa.select(Order)

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

    async def _get_list(self, limit: int, offset: int, reset_stmt: bool = True, *args, **kwargs) -> List[Order]:
        res = await (
            self.session.execute(
                self._stmt.order_by(sa.desc(Order.created_at))
                .limit(limit)
                .offset(offset)
            )
        )
        if reset_stmt:
            self._reset_stmt()
        return list(res.scalars())

    async def _count(self) -> int:
        stmt = sa.select(sa.func.count(1)).select_from(Order)

        if self._stmt.whereclause:
            stmt = stmt.where(*self._stmt.whereclause)

        res = await self.session.execute(stmt)
        self._reset_stmt()
        return res.scalar()

    async def _exists(self) -> bool:
        raise NotImplementedError

    def _related_to_user_tg_id(self, user_tg_id: int) -> Self:
        self._stmt = self._stmt.where(Order.user_tg_id==user_tg_id)
        return self

    def _related_to_supplier_tg_id(self, supplier_tg_id: int) -> Self:
        self._stmt = self._stmt.where(Order.supplier_tg_id==supplier_tg_id)
        return self
