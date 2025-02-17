from src.app.bootstrap import inject_dependencies
from .adapters.orm import start_mappers
from .service.unit_of_work import AbstractUnitOfWork, SqlAlchemyUnitOfWork
from .service import handlers, MessageBus


def get_bootstrap(
        start_orm: bool = True,
        uow: AbstractUnitOfWork = SqlAlchemyUnitOfWork()
):
    if start_orm:
        start_mappers()

    dependencies = {'uow': uow}

    injected_command_handlers = {
        command_type: inject_dependencies(handler, dependencies)
        for command_type, handler in handlers.COMMAND_HANDLERS.items()
    }

    return MessageBus(uow=uow, command_handlers=injected_command_handlers)


bootstrap = get_bootstrap()

