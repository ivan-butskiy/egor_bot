import abc

from sqlalchemy.orm import Session

from src.infrastructure.db.session import SESSION_FACTORY
from src.domain.users.adapters.repository import AbstractRepository, SqlAlchemyRepository


class AbstractUnitOfWork(abc.ABC):
    users: AbstractRepository

    async def __aenter__(self) -> 'AbstractUnitOfWork':
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.rollback()

    async def commit(self) -> None:
        await self._commit()

    @abc.abstractmethod
    async def rollback(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def _commit(self):
        raise NotImplementedError


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory: Session = SESSION_FACTORY):
        self.session_factory = session_factory

    async def __aenter__(self) -> 'AbstractUnitOfWork':
        self.session = self.session_factory()
        self.users = SqlAlchemyRepository(self.session)
        return await super().__aenter__()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await super().__aexit__(exc_type, exc_val, exc_tb)
        await self.session.close()

    async def _commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
