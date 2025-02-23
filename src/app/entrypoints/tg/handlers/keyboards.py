from aiogram import types

from src.app.entrypoints.tg.handlers import commands as cmd
from src.app.entrypoints.tg.handlers.callbacks import BackCallback
from src.users import User


def get_to_the_head_kb():
    btn = types.KeyboardButton(text=cmd.StartKbCommands.to_the_head)
    return types.ReplyKeyboardMarkup(keyboard=[[btn]])


def get_start_kb(user: User) -> types.ReplyKeyboardMarkup:
    buttons = [
        [types.KeyboardButton(text=cmd.StartKbCommands.suppliers)],
        [types.KeyboardButton(text=cmd.StartKbCommands.orders)],
    ]

    if user.is_admin:
        buttons.append([types.KeyboardButton(text=cmd.StartKbCommands.users)])
    return types.ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        input_field_placeholder='Оберіть дію:',
        one_time_keyboard=True
    )


def get_inline_nav_keyboard(entity: str):
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text='⬅ Назад', callback_data=BackCallback(entity=entity).pack())]
        ]
    )
