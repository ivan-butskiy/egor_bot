from typing import Tuple, List

from src.orders.service.unit_of_work import AbstractUnitOfWork
from src.orders import Order
from src.users import User


async def get_orders(
        uow: AbstractUnitOfWork,
        user: User,
        offset: int = 0,
        limit: int = 10,
        supplier_tg_id: int = None
) -> Tuple[List[Order], int]:
    async with uow:
        query = uow.orders
        if not user.is_admin:
            query = query.related_to_user_tg_id(user.tg_id)
        if supplier_tg_id:
            query = query.related_to_supplier_tg_id(supplier_tg_id)

        items = await query.get_list(limit, offset, reset_stmt=False)
        count = await query.count()
        return items, count

async def get_order(uow: AbstractUnitOfWork, id_: int) -> Order:
    async with uow:
        return await uow.orders.get(id_)


async def get_orders_count(uow: AbstractUnitOfWork) -> int:
    async with uow:
        return await uow.orders.count()
