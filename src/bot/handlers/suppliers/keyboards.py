from typing import List

from aiogram import types

from src.bot.handlers.suppliers import commands as cmd
from src.domain.suppliers import Supplier
from src.domain.users import User
from . import filters


def get_suppliers_kb(count: int) -> types.ReplyKeyboardMarkup:
    buttons = []

    if count:
        buttons.append([types.KeyboardButton(text=cmd.SuppliersCommands.get_suppliers)])

    buttons.append([types.KeyboardButton(text=cmd.SuppliersCommands.create_supplier)])

    return types.ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        one_time_keyboard=True
    )


def get_suppliers_list_kb(
        user: User,
        items: List[Supplier],
        count: int,
        page: int = 1,
        page_size: int = 10
) -> types.InlineKeyboardMarkup:

    buttons = [
        [types.InlineKeyboardButton(
            text=i.title if user.is_admin else i.alias,
            callback_data=filters.SupplierItemFilter(tg_id=i.tg_id).pack())]
        for i in items
    ]

    if count > page_size:
        paginate_buttons = []
        if page != 1:
            paginate_buttons.append(
                types.InlineKeyboardButton(
                    text='⬅ Назад',
                    callback_data=filters.PaginateSuppliersFilter(page=page - 1).pack()
                )
            )
        if count > page * page_size:
            paginate_buttons.append(
                types.InlineKeyboardButton(
                    text='Вперед ➡',
                    callback_data=filters.PaginateSuppliersFilter(page=page + 1).pack()
                )
            )
        buttons.append(paginate_buttons)

    return types.InlineKeyboardMarkup(inline_keyboard=buttons)


def get_supplier_item_kb(user: User):
    buttons = [[types.KeyboardButton(text=cmd.SuppliersCommands.create_order)]]

    if user.is_admin:
        buttons.append([
            types.KeyboardButton(text=cmd.SuppliersCommands.edit_supplier),
            types.KeyboardButton(text=cmd.SuppliersCommands.remove_supplier),
        ])

    return types.ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        one_time_keyboard=True
    )
