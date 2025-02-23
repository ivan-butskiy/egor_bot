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


async def update_user(cmd: commands.UpdateUserCommand, uow: AbstractUnitOfWork):
    async with uow:
        instance: User = await uow.users.get(cmd.tg_id)

        if cmd.first_name:
            instance.first_name = cmd.first_name
        if cmd.last_name:
            instance.last_name = cmd.last_name

        await uow.commit()


async def delete_user(cmd: commands.DeleteUserCommand, uow: AbstractUnitOfWork):
    async with uow:
        await uow.users.delete(cmd.tg_id)
        await uow.commit()


COMMAND_HANDLERS = {
    commands.CreateUserCommand: create_user,
    commands.UpdateUserCommand: update_user,
    commands.DeleteUserCommand: delete_user
}

EVENT_HANDLERS = {}