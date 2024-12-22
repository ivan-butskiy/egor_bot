from src.domain.users.service.unit_of_work import AbstractUnitOfWork


async def get_user(tg_id, uow: AbstractUnitOfWork):
    async with uow:
        return await uow.users.get(tg_id)
