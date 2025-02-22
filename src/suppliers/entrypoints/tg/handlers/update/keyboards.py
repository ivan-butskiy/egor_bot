from aiogram import types

from .commands import UpdateSupplierCommands
from .filters import EditSupplierFilter, EditSupplierActionsEnum


def get_edit_supplier_kb(supplier_tg_id: int) -> types.InlineKeyboardMarkup:
    text_actions = (
        (UpdateSupplierCommands.contact, EditSupplierActionsEnum.contact),
        (UpdateSupplierCommands.title, EditSupplierActionsEnum.title),
        (UpdateSupplierCommands.alias, EditSupplierActionsEnum.alias),
        (UpdateSupplierCommands.cancel, EditSupplierActionsEnum.cancel)
    )

    buttons = [
        [types.InlineKeyboardButton(text=c,
                                    callback_data=EditSupplierFilter(tg_id=supplier_tg_id, action=a).pack())]
        for c, a in text_actions
    ]

    return types.InlineKeyboardMarkup(inline_keyboard=buttons)
