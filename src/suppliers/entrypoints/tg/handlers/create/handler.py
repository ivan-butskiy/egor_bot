from aiogram import Router, F
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown

from src.users import User
from ... import commands as suppliers_cmd
from src.app.entrypoints.tg.utils import auth_decorator
from src.app.entrypoints.tg.handlers import keyboards as base_kbs
from .states import UserState


router = Router(name=__name__)


@router.message(F.text == suppliers_cmd.SuppliersCommands.create_supplier)
@auth_decorator
async def handle_create_supplier(message: types.Message, state: FSMContext):
    text = markdown.text(
        markdown.hbold('Крок 1/4'),
        markdown.text('Введіть нікнейм в форматі "@nickname":'),
        sep='\n'
    )

    await state.set_state(UserState.username)
    await message.answer(text=text)


@router.message(UserState.username, F.text)
async def handle_username(message: types.Message, state: FSMContext):
    text = markdown.text(
        markdown.hbold('Крок 2/4'),
        markdown.text('Введіть назву:'),
        sep='\n'
    )

    # user = await get_tg_user(UserState.username)
    # d = 1

    await state.update_data(username=message.text)
    await state.set_state(UserState.title)
    await message.answer(text=text)


@router.message(UserState.title, F.text)
async def handle_title(message: types.Message, state: FSMContext):
    text = markdown.text(
        markdown.hbold('Крок 3/4'),
        markdown.text('Введіть псевдонім:'),
        sep='\n'
    )

    await state.update_data(title=message.text)
    await state.set_state(UserState.alias)
    await message.answer(text=text)


@router.message(UserState.alias, F.text)
@auth_decorator
async def handle_alias(message: types.Message, state: FSMContext, user: User):
    await state.update_data(alias=message.text)
    await message.answer(
        text='Додано!',
        reply_markup=base_kbs.get_start_kb(user)
    )
    await state.clear()
