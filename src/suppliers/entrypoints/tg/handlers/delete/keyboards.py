from aiogram import types

from .commands import DeleteSupplierCommands
from .filters import DeleteSupplierFilter, DeleteSupplierActionsEnum


def get_delete_supplier_keyboard(supplier_tg_id: int) -> types.InlineKeyboardMarkup:
    text_actions = (
        (DeleteSupplierCommands.approve, DeleteSupplierActionsEnum.approve),
        (DeleteSupplierCommands.reject, DeleteSupplierActionsEnum.reject),
    )

    buttons = [
        [types.InlineKeyboardButton(text=c,
                                    callback_data=DeleteSupplierFilter(tg_id=supplier_tg_id, action=a).pack())]
        for c, a in text_actions
    ]

    return types.InlineKeyboardMarkup(inline_keyboard=buttons)
