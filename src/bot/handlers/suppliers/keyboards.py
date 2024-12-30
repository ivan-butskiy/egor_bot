from typing import List

from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.bot.handlers.suppliers import commands as cmd
from src.domain.suppliers import Supplier
from src.domain.users import User


def get_suppliers_keyboard(count: int) -> types.ReplyKeyboardMarkup:
    buttons = []

    if count:
        buttons.append([types.KeyboardButton(text=cmd.SuppliersCommands.get_suppliers)])

    buttons.append([types.KeyboardButton(text=cmd.SuppliersCommands.add_supplier)])

    return types.ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        one_time_keyboard=True
    )


def get_list_suppliers_list_keyboard(
        items: List[Supplier],
        user: User
) -> types.InlineKeyboardMarkup:
    buttons = [
        types.InlineKeyboardButton(
            text=i.title if user.is_admin else i.alias,
            callback_data=str(i.id)
        )
        for i in items
    ]
    return InlineKeyboardBuilder(markup=[buttons]).as_markup()
