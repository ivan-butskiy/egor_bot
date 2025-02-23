from typing import Tuple, List

from src.orders.service.unit_of_work import AbstractUnitOfWork
from src.orders import Order


async def get_orders(
        uow: AbstractUnitOfWork,
        offset: int = 0,
        limit: int = 10,
) -> Tuple[List[Order], int]:
    async with uow:
        items = await uow.orders.get_list(limit, offset)
        count = await uow.orders.count()
        return items, count


async def get_order(uow: AbstractUnitOfWork, id_: int) -> Order:
    async with uow:
        return await uow.orders.get(id_)


async def get_orders_count(uow: AbstractUnitOfWork) -> int:
    async with uow:
        return await uow.orders.count()
