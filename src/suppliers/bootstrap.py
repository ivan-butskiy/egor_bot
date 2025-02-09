from .adapters.orm import start_mappers
from .service.unit_of_work import AbstractUnitOfWork, SqlAlchemyUnitOfWork
from .service.message_bus import MessageBus


def bootstrap(
        start_orm: bool = True,
        uow: AbstractUnitOfWork = SqlAlchemyUnitOfWork()
):
    if start_orm:
        start_mappers()

    # dependencies = {'uow': uow}

    return MessageBus(uow=uow)
