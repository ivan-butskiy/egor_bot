from typing import List

from aiogram import types

from src.suppliers import Supplier
from src.users import User
from src.suppliers.entrypoints.tg.filters import (
    PaginateSuppliersFilter,
    SupplierItemFilter,
    SupplierItemActionEnum
)
from . import commands as cmd


def get_suppliers_kb(count: int) -> types.ReplyKeyboardMarkup:
    buttons = []

    if count:
        buttons.append([types.KeyboardButton(text=cmd.SuppliersCommands.get_suppliers)])

    buttons.append([types.KeyboardButton(text=cmd.SuppliersCommands.create_supplier)])

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
        [
            types.InlineKeyboardButton(
                text=i.title if user.is_admin else i.alias,
                callback_data=SupplierItemFilter(
                    tg_id=i.tg_id,
                    action=SupplierItemActionEnum.get)
                .pack()
            )
        ]
        for i in items
    ]

    if count > page_size:
        paginate_buttons = []
        if page != 1:
            paginate_buttons.append(
                types.InlineKeyboardButton(
                    text='⬅ Назад',
                    callback_data=PaginateSuppliersFilter(page=page - 1).pack()
                )
            )
        if count > page * page_size:
            paginate_buttons.append(
                types.InlineKeyboardButton(
                    text='Вперед ➡',
                    callback_data=PaginateSuppliersFilter(page=page + 1).pack()
                )
            )
        buttons.append(paginate_buttons)

    return types.InlineKeyboardMarkup(inline_keyboard=buttons)


def get_supplier_item_kb(user: User, supplier: Supplier) -> types.InlineKeyboardMarkup:
    buttons = [
        [types.InlineKeyboardButton(
            text=cmd.SuppliersCommands.create_order,
            callback_data=SupplierItemFilter(tg_id=supplier.tg_id, action=SupplierItemActionEnum.create_order).pack()
        )]
    ]

    if user.is_admin:
        edit_btn = types.InlineKeyboardButton(
            text=cmd.SuppliersCommands.edit_supplier,
            callback_data=SupplierItemFilter(tg_id=supplier.tg_id, action=SupplierItemActionEnum.edit).pack()
        )

        delete_btn = types.InlineKeyboardButton(
            text=cmd.SuppliersCommands.delete_supplier,
            callback_data=SupplierItemFilter(tg_id=supplier.tg_id, action=SupplierItemActionEnum.delete).pack()
        )
        buttons.append([edit_btn])
        buttons.append([delete_btn])

    return types.InlineKeyboardMarkup(inline_keyboard=buttons)
