import abc

from sqlalchemy.orm import Session

from src.app.service.unit_of_work import AbstractUnitOfWork as _AbstractUnitOfWork
from src.app.infrastructure.db.session import SESSION_FACTORY
from src.orders.adapters.repository import AbstractRepository, SQLAlchemyRepository


class AbstractUnitOfWork(_AbstractUnitOfWork, abc.ABC):
    orders: AbstractRepository


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):

    def __init__(self, session: Session = SESSION_FACTORY):
        self.session_factory = session

    async def __aenter__(self) -> 'AbstractUnitOfWork':
        self.session = self.session_factory()
        self.orders = SQLAlchemyRepository(self.session)
        return await super().__aenter__()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await super().__aexit__(exc_type, exc_val, exc_tb)
        await self.session.close()

    async def _commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
