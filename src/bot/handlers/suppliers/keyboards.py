from typing import List

from aiogram import types

from src.bot.handlers.suppliers import commands as cmd
from src.domain.suppliers import Supplier
from src.domain.users import User


def get_suppliers_kb(count: int) -> types.ReplyKeyboardMarkup:
    buttons = []

    if count:
        buttons.append([types.KeyboardButton(text=cmd.SuppliersCommands.get_suppliers)])

    buttons.append([types.KeyboardButton(text=cmd.SuppliersCommands.add_supplier)])

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
            callback_data=f'{cmd.SuppliersCallback.supplier_item}{i.id}')]
        for i in items
    ]

    if count > page_size:
        paginate_buttons = []
        if page != 1:
            paginate_buttons.append(
                types.InlineKeyboardButton(
                    text='⬅ назад',
                    callback_data=f'{cmd.SuppliersCallback.paginate_suppliers}{page - 1}'
                )
            )
        if count > page * page_size:
            paginate_buttons.append(
                types.InlineKeyboardButton(
                    text='вперед ➡',
                    callback_data=f'{cmd.SuppliersCallback.paginate_suppliers}{page + 1}'
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
