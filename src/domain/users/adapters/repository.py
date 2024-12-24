import abc
from typing import Set

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.users.domain import User


class AbstractRepository(abc.ABC):

    def __init__(self):
        self.seen = set()  # type: Set[User]

    async def add(self, user: User):
        await self._add(user)
        self.seen.add(user)

    async def get(self, tg_id: int) -> User:
        user = await self._get(tg_id)
        if user:
            self.seen.add(user)
        return user

    # @abc.abstractmethod
    async def _add(self, user: User):
        raise NotImplementedError

    # @abc.abstractmethod
    async def _get(self, tg_id) -> User:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session: AsyncSession):
        super().__init__()
        self.session = session

    async def _add(self, user: User) -> None:
        self.session.add(user)

    async def _get(self, tg_id: int) -> User | None:
        res = await (
            self.session.execute(
                sa.select(User)
                .where(User.tg_id == tg_id))
        )
        return res.scalar()
