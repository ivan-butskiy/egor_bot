from typing import List

from aiogram import types

from src.users import User
from .filters import (
    PaginateUsersFilter,
    UserItemActionEnum,
    UserItemFilter
)
from . import commands as cmd


def get_users_kb(count: int) -> types.ReplyKeyboardMarkup:
    buttons = []

    if count:
        buttons.append([types.KeyboardButton(text=cmd.UsersCommand.get_users)])

    buttons.append([types.KeyboardButton(text=cmd.UsersCommand.create_user)])

    return types.ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        one_time_keyboard=True
    )


def get_users_list_kb(
        items: List[User],
        count: int,
        page: int = 1,
        page_size: int = 10
) -> types.InlineKeyboardMarkup:

    buttons = [
        [
            types.InlineKeyboardButton(
                text=i.button_repr,
                callback_data=UserItemFilter(
                    tg_id=i.tg_id,
                    action=UserItemActionEnum.get)
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
                    callback_data=PaginateUsersFilter(page=page - 1).pack()
                )
            )
        if count > page * page_size:
            paginate_buttons.append(
                types.InlineKeyboardButton(
                    text='Вперед ➡',
                    callback_data=PaginateUsersFilter(page=page + 1).pack()
                )
            )
        buttons.append(paginate_buttons)

    return types.InlineKeyboardMarkup(inline_keyboard=buttons)


def get_user_item_kb(user: User) -> types.InlineKeyboardMarkup:
    edit_btn = types.InlineKeyboardButton(
        text=cmd.UsersCommand.edit_user,
        callback_data=UserItemFilter(tg_id=user.tg_id, action=UserItemActionEnum.edit).pack()
    )

    delete_btn = types.InlineKeyboardButton(
        text=cmd.UsersCommand.delete_user,
        callback_data=UserItemFilter(tg_id=user.tg_id, action=UserItemActionEnum.delete).pack()
    )

    buttons = [[edit_btn]]
    if not user.is_admin:
        buttons.append([delete_btn])

    return types.InlineKeyboardMarkup(inline_keyboard=buttons)
