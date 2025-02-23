from aiogram import Router, F
from aiogram import types
from aiogram.utils import markdown

from src.app.entrypoints.tg.utils import auth_decorator
from src.app.entrypoints.tg.handlers import keyboards as base_kbs
from src.users import User
from src.users.domain.commands import DeleteUserCommand
from src.users.bootstrap import bootstrap
from src.users.entrypoints.tg.filters import UserItemFilter, UserItemActionEnum
from .keyboards import get_delete_user_keyboard
from .filters import DeleteUserFilter, DeleteUserActionsEnum


router = Router(name=__name__)


@router.callback_query(UserItemFilter.filter(F.action == UserItemActionEnum.delete))
async def handle_delete_user(
        callback_query: types.CallbackQuery,
        callback_data: UserItemFilter
) -> None:
    text = markdown.text(
        markdown.hbold('Підтвердіть дію.\n'),
        markdown.text('Ви впевнені, що бажаєте видалити користувача? '
                      'Разом з ним будуть видалені пов\'язані замовлення. '
                      'Після видалення скасувати цю дію буде неможливо'),
        sep='\n'
    )

    await callback_query.answer()
    await callback_query.bot.send_message(
        chat_id=callback_query.from_user.id,
        text=text,
        reply_markup=get_delete_user_keyboard(callback_data.tg_id)
    )


@router.callback_query(DeleteUserFilter.filter(F.action == DeleteUserActionsEnum.approve))
@auth_decorator
async def handle_approve_delete(
        callback_query: types.CallbackQuery,
        callback_data: DeleteUserFilter,
        user: User
):
    cmd = DeleteUserCommand(tg_id=callback_data.tg_id)
    await bootstrap.handle(cmd)
    await callback_query.answer()
    await callback_query.bot.send_message(
        chat_id=callback_query.from_user.id,
        text='Користувач успішно видалений.',
        reply_markup=base_kbs.get_start_kb(user)
    )


@router.callback_query(DeleteUserFilter.filter(F.action == DeleteUserActionsEnum.reject))
@auth_decorator
async def handle_reject_delete(callback_query: types.CallbackQuery, user: User):
    await callback_query.answer()
    await callback_query.bot.send_message(
        chat_id=callback_query.from_user.id,
        text='Видалення скасовано.',
        reply_markup=base_kbs.get_start_kb(user)
    )
