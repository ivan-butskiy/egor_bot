import abc
from typing import Set

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.adapters.repository import BaseAbstractRepository
from src.users.domain import User


class AbstractRepository(BaseAbstractRepository, abc.ABC):
    seen: Set[User]


class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session: AsyncSession):
        super().__init__()
        self.session = session

    async def _add(self, user: User) -> None:
        self.session.add(user)

    async def _get(self, tg_id: int, exclude_id: int = None) -> User | None:
        stmt = sa.select(User).where(User.tg_id == tg_id)

        if exclude_id:
            stmt = stmt.where(User.tg_id != exclude_id)

        res = await self.session.execute(stmt)
        return res.scalar()

    async def _delete(self, tg_id: int) -> None:
        stmt = sa.delete(User).where(User.tg_id == tg_id)
        await self.session.execute(stmt)

    async def _get_list(self, limit: int, offset: int):
        res = await (
            self.session.execute(
                sa.select(User)
                .limit(limit)
                .offset(offset)
            )
        )
        return list(res.scalars())

    async def _count(self) -> int:
        stmt = (
            sa.select(sa.func.count(1))
            .select_from(User)
        )

        res = await self.session.execute(stmt)
        return res.scalar()

    async def _exists(self) -> bool:
        stmt = (
            sa.select(1)
            .select_from(User)
            .exists()
        )
        res = await self.session.execute(sa.select(stmt))
        return res.scalar()
