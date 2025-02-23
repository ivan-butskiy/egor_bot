from aiogram import types

from .commands import DeleteUserCommands
from .filters import DeleteUserFilter, DeleteUserActionsEnum


def get_delete_user_keyboard(user_tg_id: int) -> types.InlineKeyboardMarkup:
    text_actions = (
        (DeleteUserCommands.approve, DeleteUserActionsEnum.approve),
        (DeleteUserCommands.reject, DeleteUserActionsEnum.reject),
    )

    buttons = [
        [types.InlineKeyboardButton(text=c,
                                    callback_data=DeleteUserFilter(tg_id=user_tg_id, action=a).pack())]
        for c, a in text_actions
    ]

    return types.InlineKeyboardMarkup(inline_keyboard=buttons)
