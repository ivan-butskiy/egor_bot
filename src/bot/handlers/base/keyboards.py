from aiogram import types
from src.bot.handlers.base import commands as cmd

_select_action_buttons = [
    [types.KeyboardButton(text='Оформити замовлення')],
]


select_action_keyboard = types.ReplyKeyboardMarkup(
    keyboard=_select_action_buttons,
    resize_keyboard=True,
    input_field_placeholder='Оберіть дію'
)


start_admin_keyboard = types.ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text=cmd.StartKbCommands.orders)],
        [types.KeyboardButton(text=cmd.StartKbCommands.suppliers)],
        [types.KeyboardButton(text=cmd.StartKbCommands.suppliers)],
    ],
    resize_keyboard=True,
    input_field_placeholder='Оберіть дію'
)


start_manager_keyboard = types.ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text=cmd.StartKbCommands.create_order)],
        [types.KeyboardButton(text=cmd.StartKbCommands.order_history)],
    ],
    resize_keyboard=True,
    input_field_placeholder='Оберіть дію'
)

