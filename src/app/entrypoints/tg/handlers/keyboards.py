from aiogram import types

from src.app.entrypoints.tg.handlers import commands as cmd
from src.users import User


def get_to_the_head_kb():
    btn = types.KeyboardButton(text=cmd.StartKbCommands.to_the_head)
    return types.ReplyKeyboardMarkup(keyboard=[[btn]])


def get_start_kb(user: User) -> types.ReplyKeyboardMarkup:
    if user.is_admin:
        return types.ReplyKeyboardMarkup(
            keyboard=[
                [types.KeyboardButton(text=cmd.StartKbCommands.suppliers),
                 types.KeyboardButton(text=cmd.StartKbCommands.orders)],
            ],
            resize_keyboard=True,
            input_field_placeholder='Оберіть дію',
            one_time_keyboard=True
        )
    return types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text=cmd.StartKbCommands.create_order)],
            [types.KeyboardButton(text=cmd.StartKbCommands.order_history)],
        ],
        resize_keyboard=True,
        input_field_placeholder='Оберіть дію'
    )
