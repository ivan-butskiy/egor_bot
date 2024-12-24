import abc

from sqlalchemy.orm import Session

from src.app.service.unit_of_work import AbstractUnitOfWork as _AbstractUnitOfWork
from src.infrastructure.db.session import SESSION_FACTORY
from src.domain.suppliers.adapters.repository import AbstractRepository, SqlAlchemyRepository


class AbstractUnitOfWork(_AbstractUnitOfWork, abc.ABC):
    suppliers: AbstractRepository


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):

    def __init__(self, session_factory: Session = SESSION_FACTORY):
        self.session_factory = session_factory

    async def __aenter__(self) -> 'AbstractUnitOfWork':
        self.session = self.session_factory()
        self.suppliers = SqlAlchemyRepository(self.session)
        return await super().__aenter__()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await super().__aexit__(exc_type, exc_val, exc_tb)
        await self.session.close()

    async def _commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
