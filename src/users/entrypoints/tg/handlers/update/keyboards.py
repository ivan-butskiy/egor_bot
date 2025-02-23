from aiogram import types

from .commands import UpdateUserCommands
from .filters import EditUserFilter, EditUserActionsEnum


def get_edit_user_kb(user_tg_id: int) -> types.InlineKeyboardMarkup:
    text_actions = (
        (UpdateUserCommands.first_name, EditUserActionsEnum.first_name),
        (UpdateUserCommands.last_name, EditUserActionsEnum.last_name),
        (UpdateUserCommands.cancel, EditUserActionsEnum.cancel),
    )

    buttons = [
        [types.InlineKeyboardButton(text=c,
                                    callback_data=EditUserFilter(tg_id=user_tg_id, action=a).pack())]
        for c, a in text_actions
    ]

    return types.InlineKeyboardMarkup(inline_keyboard=buttons)
