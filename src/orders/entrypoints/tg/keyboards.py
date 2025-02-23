from typing import List

from aiogram import types
from aiogram.utils import markdown

from src.users import User
from src.orders import Order
from src.orders.entrypoints.tg.filters import (
    PaginateOrdersFilter,
    OrderItemFilter,
    OrderItemActionEnum
)


def get_orders_list_kb(
        user: User,
        items: List[Order],
        count: int,
        page: int = 1,
        page_size: int = 10
) -> types.InlineKeyboardMarkup:

    def get_btn_text(order: Order) -> str:
        if user.is_admin:
            return markdown.text(
                markdown.hbold(order.id),
                markdown.text(
                    markdown.text('Постачальник:'),
                    markdown.italic(order.supplier.title),
                    markdown.italic(f'({order.supplier.alias})'),
                    sep=' '
                ),
                sep='\n'
            )
        return markdown.text(
            markdown.hbold(order.id),
            markdown.text(
                markdown.text('Постачальник: '),
                markdown.italic(order.supplier.alias)
            ),
            sep='\n'
        )

    buttons = [
        [
            types.InlineKeyboardButton(
                text=get_btn_text(i),
                callback_data=OrderItemFilter(
                    id=i.id,
                    action=OrderItemActionEnum.get)
                .pack()
            )
        ]
        for i in items
    ]

    if count > page_size:
        paginate_buttons = []
        if page != 1:
            paginate_buttons.append(
                types.InlineKeyboardButton(
                    text='⬅ Назад',
                    callback_data=PaginateOrdersFilter(page=page - 1).pack()
                )
            )
        if count > page * page_size:
            paginate_buttons.append(
                types.InlineKeyboardButton(
                    text='Вперед ➡',
                    callback_data=PaginateOrdersFilter(page=page + 1).pack()
                )
            )
        buttons.append(paginate_buttons)

    return types.InlineKeyboardMarkup(inline_keyboard=buttons)
