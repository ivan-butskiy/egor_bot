from src.users.service.unit_of_work import AbstractUnitOfWork
from src.users.domain import commands
from src.users.domain.model import User


async def create_user(cmd: commands.CreateUserCommand, uow: AbstractUnitOfWork):
    async with uow:
        instance = User(
            tg_id=cmd.tg_id,
            first_name=cmd.first_name,
            last_name=cmd.last_name,
            type=cmd.type
        )

        await uow.users.add(instance)
        await uow.commit()


COMMAND_HANDLERS = {
    commands.CreateUserCommand: create_user
}

EVENT_HANDLERS = {}