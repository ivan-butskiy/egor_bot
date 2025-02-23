from aiogram import Router, F, types
from aiogram.utils import markdown

from src.app.entrypoints.tg.handlers.keyboards import get_start_kb
from src.app.entrypoints.tg.utils import auth_decorator
from src.app.entrypoints.tg.handlers import commands as base_cmd
from src.users import User
from src.orders.bootstrap import bootstrap
from src.orders import views
from src.orders.entrypoints.tg import keyboards as kb
from src.orders.entrypoints.tg.filters import (
    OrderItemFilter,
    PaginateOrdersFilter,
    OrderItemActionEnum
)
from .create import router as create_router


router = Router(name=__name__)


@router.message(F.text == base_cmd.StartKbCommands.orders)
@auth_decorator
async def handle_orders(message: types.Message, user: User):
    items, count = await views.get_orders(bootstrap.uow, user)

    if not count:
        await message.answer(
            text='Наразі немає жодного замовлення.',
            reply_markup=get_start_kb(user)
        )
        return
    await message.answer(
        text='Оберіть замовлення:',
        reply_markup=kb.get_orders_list_kb(user, items, count)
    )


router.include_routers(
    create_router
)
