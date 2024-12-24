from aiogram import types

from src.bot.handlers.base import commands as cmd
from src.domain.users import User


def get_start_keyboard(user: User):
    if user.is_admin:
        return types.ReplyKeyboardMarkup(
            keyboard=[
                # [types.KeyboardButton(text=cmd.StartKbCommands.orders)],
                [types.KeyboardButton(text=cmd.StartKbCommands.suppliers)],
            ],
            resize_keyboard=True,
            input_field_placeholder='Оберіть дію'
        )
    return types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text=cmd.StartKbCommands.create_order)],
            [types.KeyboardButton(text=cmd.StartKbCommands.order_history)],
        ],
        resize_keyboard=True,
        input_field_placeholder='Оберіть дію'
    )
