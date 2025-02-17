import logging
from typing import Dict, Type, Union, Callable, List

from src.app.service.unit_of_work import AbstractUnitOfWork
from src.app.domain.commands import BaseCommand
from src.app.domain.events import BaseEvent


logger = logging.getLogger(__name__)

Message = Union[BaseCommand, BaseEvent]


class BaseMessageBus:
    def __init__(
            self,
            uow: AbstractUnitOfWork,
            event_handlers: Dict[Type[BaseEvent], List[Callable]] = None,
            command_handlers: Dict[Type[BaseCommand], Callable] = None
    ):
        self.uow = uow
        self.event_handlers = event_handlers or {}
        self.command_handlers = command_handlers or {}

    async def handle(self, message: Message):
        self.queue = [message]
        while self.queue:
            message = self.queue.pop(0)
            if isinstance(message, BaseEvent):
                await self.handle_event(message)
            elif isinstance(message, BaseCommand):
                await self.handle_command(message)
            else:
                raise Exception(f'{message} was not an Event or Command')

    async def handle_event(self, event: BaseEvent):
        for handler in self.event_handlers[type(event)]:
            try:
                logger.debug(f'handling event {event} with handler {handler}')
                await handler(event)
                # self.queue.extend(self.uow.collect_new_events())
            except Exception:
                logger.exception(f'Exception handling event {event}')
                continue

    async def handle_command(self, command: BaseCommand):
        logger.debug(f'handling command {command}')
        try:
            handler = self.command_handlers[type(command)]
            await handler(command)
            # self.queue.extend(self.uow.collect_new_events())
        except Exception:
            logger.exception(f'Exception handling command {command}')
            raise
