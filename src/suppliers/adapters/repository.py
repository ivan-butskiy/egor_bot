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

    async def get(self, id_: int, exclude_id: int = None) -> Supplier:
        user = await self._get(id_, exclude_id)
        if user:
            self.seen.add(user)
        return user

    async def delete(self, id_: int) -> None:
        await self._delete(id_)

    async def get_list(self, limit: int, offset: int) -> List[Supplier]:
        res = await self._get_list(limit, offset)
        self.seen.union(res)
        return await self._get_list(limit, offset)

    async def count(self) -> int:
        return await self._count()

    async def exists(self) -> bool:
        return await self._exists()

    async def exists_by_title(self, title: str, exclude_tg_id: int = None) -> bool:
        return await self._exists_by_title(title, exclude_tg_id)

    async def exists_by_alias(self, alias: str, exclude_tg_id: int = None) -> bool:
        return await self._exists_by_alias(alias, exclude_tg_id)

    @abc.abstractmethod
    async def _add(self, user: Supplier):
        raise NotImplementedError

    @abc.abstractmethod
    async def _get(self, tg_id, exclude_id: int = None) -> Supplier:
        raise NotImplementedError

    @abc.abstractmethod
    async def _delete(self, id_: int) -> None:
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
    async def _exists_by_title(self, title: str, exclude_tg_id: int = None) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    async def _exists_by_alias(self, title: str, exclude_tg_id: int = None) -> bool:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session: AsyncSession):
        super().__init__()
        self.session = session

    async def _add(self, supplier: Supplier) -> None:
        self.seen.add(supplier)
        self.session.add(supplier)

    async def _get(self, tg_id: int, exclude_id: int = None) -> Supplier:
        stmt = sa.select(Supplier).where(Supplier.tg_id == tg_id)
        if exclude_id:
            stmt = stmt.where(Supplier.tg_id != exclude_id)
        res = await self.session.execute(stmt)
        return res.scalar()

    async def _delete(self, tg_id: int) -> None:
        stmt = sa.delete(Supplier).where(Supplier.tg_id == tg_id)
        await self.session.execute(stmt)

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

    async def _exists_by_title(self, title: str, exclude_tg_id: int = None) -> bool:
        stmt = (
            sa.select(sa.true())
            .select_from(Supplier)
            .where(Supplier.title == title)
            .exists()
        )

        if exclude_tg_id:
            stmt = stmt.where(Supplier.tg_id != exclude_tg_id)

        res = await self.session.execute(sa.select(stmt))
        return res.scalar()

    async def _exists_by_alias(self, alias: str, exclude_tg_id: int = None) -> bool:
        stmt = (
            sa.select(sa.true())
            .select_from(Supplier)
            .where(Supplier.alias == alias)
            .exists()
        )

        if exclude_tg_id:
            stmt = stmt.where(Supplier.tg_id != exclude_tg_id)

        res = await self.session.execute(sa.select(stmt))
        return res.scalar()
