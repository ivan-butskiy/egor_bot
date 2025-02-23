from aiogram import Router, F
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown

from src.app.entrypoints.tg.utils import auth_decorator
from src.app.entrypoints.tg.handlers import keyboards as base_kbs
from src.users import User
from src.users.entrypoints.tg.handlers.states import UpdateUserState
from src.users.entrypoints.tg.filters import UserItemFilter, UserItemActionEnum
from src.users.bootstrap import bootstrap
from src.users.domain.commands import UpdateUserCommand
from .keyboards import get_edit_user_kb
from .filters import EditUserFilter, EditUserActionsEnum


router = Router(name=__name__)


@router.callback_query(UserItemFilter.filter(F.action == UserItemActionEnum.edit))
async def handle_edit_supplier(
        callback_query: types.CallbackQuery,
        callback_data: UserItemFilter,
        state: FSMContext
) -> None:
    await state.update_data({UpdateUserState.update_user_tg_id: callback_data.tg_id})

    text = markdown.text(
        'Будь ласка, оберіть, що ви хочете змінити для користувача:'
    )

    await callback_query.answer()
    await callback_query.bot.send_message(
        chat_id=callback_query.from_user.id,
        text=text,
        reply_markup=get_edit_user_kb(callback_data.tg_id)
    )


@router.callback_query(EditUserFilter.filter(F.action == EditUserActionsEnum.first_name))
async def set_first_name_state(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    await callback_query.answer()
    await state.set_state(UpdateUserState.update_user_first_name)
    text = markdown.text("Введіть бажане ім'я для користувача:")
    await callback_query.bot.send_message(
        chat_id=callback_query.from_user.id,
        text=text
    )


@router.callback_query(EditUserFilter.filter(F.action == EditUserActionsEnum.last_name))
async def set_last_name_state(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    await callback_query.answer()
    await state.set_state(UpdateUserState.update_user_last_name)
    text = markdown.text("Введіть бажане прізвище для користувача:")
    await callback_query.bot.send_message(
        chat_id=callback_query.from_user.id,
        text=text
    )


@router.callback_query(EditUserFilter.filter(F.action == EditUserActionsEnum.cancel))
@auth_decorator
async def set_cancel_state(
        callback_query: types.CallbackQuery,
        state: FSMContext,
        user: User
) -> None:
    await state.clear()
    await callback_query.answer()
    await callback_query.bot.send_message(
        chat_id=callback_query.from_user.id,
        text='Редагування скасовано.',
        reply_markup=base_kbs.get_start_kb(user)
    )


@router.message(UpdateUserState.update_user_first_name, F.text)
async def handle_first_name(message: types.Message, state: FSMContext):

    data = await state.get_data()
    cmd = UpdateUserCommand(
        tg_id=data[UpdateUserState.update_user_tg_id],
        first_name=message.text
    )

    await state.clear()
    await bootstrap.handle(cmd)

    text = markdown.text(
        markdown.hbold("Ім'я користувача успішно редаговано!\n"),
        markdown.text('Оберіть, що б ви ще хотіли редагувати:'),
        sep='\n'
    )

    await message.answer(
        text=text,
        reply_markup=get_edit_user_kb(cmd.tg_id)
    )


@router.message(UpdateUserState.update_user_last_name, F.text)
async def handle_first_name(message: types.Message, state: FSMContext):
    data = await state.get_data()
    cmd = UpdateUserCommand(
        tg_id=data[UpdateUserState.update_user_tg_id],
        first_name=message.text
    )

    await state.clear()
    await bootstrap.handle(cmd)

    text = markdown.text(
        markdown.hbold('Прізвище користувача успішно редаговано!\n'),
        markdown.text('Оберіть, що б ви ще хотіли редагувати:'),
        sep='\n'
    )

    await message.answer(
        text=text,
        reply_markup=get_edit_user_kb(cmd.tg_id)
    )
