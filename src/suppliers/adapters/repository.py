import abc
from typing import Set, List

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from src.suppliers import Supplier


class AbstractRepository(abc.ABC):

    def __init__(self):
        self.seen = set()  # type: Set[Supplier]

    async def add(self, supplier: Supplier):
        await self._add(supplier)
        self.seen.add(supplier)

    async def get(self, id_: int) -> Supplier:
        user = await self._get(id_)
        if user:
            self.seen.add(user)
        return user

    async def get_list(self, limit: int, offset: int) -> List[Supplier]:
        res = await self._get_list(limit, offset)
        self.seen.union(res)
        return await self._get_list(limit, offset)

    async def count(self) -> int:
        return await self._count()

    async def exists(self) -> bool:
        return await self._exists()

    async def exists_by_title(self, title: str) -> bool:
        return await self._exists_by_title(title)

    async def exists_by_alias(self, alias: str) -> bool:
        return await self._exists_by_alias(alias)

    @abc.abstractmethod
    async def _add(self, user: Supplier):
        raise NotImplementedError

    @abc.abstractmethod
    async def _get(self, tg_id) -> Supplier:
        raise NotImplementedError

    @abc.abstractmethod
    async def _get_list(self, limit: int, offset: int):
        raise NotImplementedError

    @abc.abstractmethod
    async def _count(self) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    async def _exists(self) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    async def _exists_by_title(self, title: str) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    async def _exists_by_alias(self, title: str) -> bool:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session: AsyncSession):
        super().__init__()
        self.session = session

    async def _add(self, supplier: Supplier) -> None:
        self.seen.add(supplier)

    async def _get(self, tg_id: int) -> Supplier:
        res = await (
            self.session.execute(
                sa.select(Supplier)
                .where(Supplier.tg_id == tg_id)
            )
        )
        return res.scalar()

    async def _get_list(self, limit: int, offset: int) -> List[Supplier]:
        res = await (
            self.session.execute(
                sa.select(Supplier)
                .limit(limit)
                .offset(offset)
            )
        )
        return list(res.scalars())

    async def _count(self) -> int:
        stmt = (
            sa.select(sa.func.count(1))
            .select_from(Supplier)
        )

        res = await self.session.execute(stmt)
        return res.scalar()

    async def _exists(self) -> bool:
        stmt = (
            sa.select(1)
            .select_from(Supplier)
            .exists()
        )

        res = await self.session.execute(sa.select(stmt))
        return res.scalar()

    async def _exists_by_title(self, title: str) -> bool:
        stmt = (
            sa.select(sa.true())
            .select_from(Supplier)
            .where(Supplier.title == title)
            .exists()
        )

        res = await self.session.execute(sa.select(stmt))
        return res.scalar()

    async def _exists_by_alias(self, alias: str) -> bool:
        stmt = (
            sa.select(sa.true())
            .select_from(Supplier)
            .where(Supplier.alias == alias)
            .exists()
        )

        res = await self.session.execute(sa.select(stmt))
        return res.scalar()
