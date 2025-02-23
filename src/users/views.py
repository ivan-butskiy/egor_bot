from typing import Tuple, List

from src.users.service.unit_of_work import AbstractUnitOfWork
from src.users import User


async def get_users(
        uow: AbstractUnitOfWork,
        offset: int = 0,
        limit: int = 10,
) -> Tuple[List[User], int]:
    async with uow:
        items = await uow.users.get_list(limit, offset)
        count = await uow.users.count()
        return items, count


async def get_user(uow: AbstractUnitOfWork, tg_id: int) -> User:
    async with uow:
        return await uow.users.get(tg_id)


async def get_users_count(uow: AbstractUnitOfWork) -> int:
    async with uow:
        return await uow.users.count()


async def exists_users(uow: AbstractUnitOfWork) -> bool:
    async with uow:
        return await uow.users.exists()
