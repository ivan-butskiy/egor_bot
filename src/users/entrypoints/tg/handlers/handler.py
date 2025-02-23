from aiogram import Router, F, types, html
from aiogram.utils import markdown

from src.app.entrypoints.tg.handlers import commands as base_cmd
from src.users import views, User
from src.users.bootstrap import bootstrap
from src.users.entrypoints.tg import commands as cmd, keyboards as kb
from src.users.entrypoints.tg.filters import (
    UserItemFilter,
    PaginateUsersFilter,
    UserItemActionEnum
)


router = Router(name=__name__)


@router.message(F.text == base_cmd.StartKbCommands.users)
async def handle_users(message: types.Message):
    count = await views.get_users_count(bootstrap.uow)
    await message.answer(
        text='Оберіть дію:',
        reply_markup=kb.get_users_kb(count)
    )


@router.message(F.text == cmd.UsersCommand.get_users)
async def handle_get_users(message: types.Message):
    items, count = await views.get_users(bootstrap.uow)
    markup = kb.get_users_list_kb(items=items, count=count)
    await message.answer(
        text='Оберіть користувача:',
        reply_markup=markup
    )


@router.callback_query(PaginateUsersFilter.filter())
async def handle_paginate_users(
        callback_query: types.CallbackQuery,
        callback_data: PaginateUsersFilter,
):
    page = callback_data.page
    limit = 10
    items, count = await views.get_users(bootstrap.uow, (page - 1) * limit, limit)
    markup = kb.get_users_list_kb(items=items, count=count, page=page)
    await callback_query.message.edit_text(
        text=f'Користувачі, сторінка {page}',
        reply_markup=markup
    )


@router.callback_query(UserItemFilter.filter(F.action == UserItemActionEnum.get))
async def handle_supplier_item(
        callback_query: types.CallbackQuery,
        callback_data: UserItemFilter,
):
    user: User = await views.get_user(bootstrap.uow, callback_data.tg_id)

    text = markdown.text(
        markdown.text(user.button_repr),
        markdown.hbold(f'\nОберіть дію:'),
        sep='\n'
    )

    await callback_query.answer()
    await callback_query.bot.send_message(
        chat_id=callback_query.from_user.id,
        text=text,
        reply_markup=kb.get_user_item_kb(user)
    )
