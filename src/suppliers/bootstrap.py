import inspect

from .adapters.orm import start_mappers
from .service.unit_of_work import AbstractUnitOfWork, SqlAlchemyUnitOfWork
from .service.message_bus import MessageBus


def get_bootstrap(
        start_orm: bool = True,
        uow: AbstractUnitOfWork = SqlAlchemyUnitOfWork()
):
    if start_orm:
        start_mappers()

    # dependencies = {'uow': uow}

    return MessageBus(uow=uow)


def inject_dependencies(handler, dependencies):
    params = inspect.signature(handler).parameters
    deps = {
        name: dependency
        for name, dependency in dependencies.items()
        if name in params
    }
    return lambda message: handler(message, **deps)


bootstrap = get_bootstrap()

