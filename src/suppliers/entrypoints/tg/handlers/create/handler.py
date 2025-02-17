from aiogram import Router, F
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown

from src.app.infrastructure.tg.client import find_user
from src.app.entrypoints.tg.utils import auth_decorator
from src.app.entrypoints.tg.handlers import keyboards as base_kbs, callbacks as base_cbs
from src.users import User
from src.suppliers import views
from src.suppliers.bootstrap import bootstrap
from src.suppliers.entrypoints.tg import commands as suppliers_cmd
from .states import CreateSupplierState


router = Router(name=__name__)


async def _handle_create_supplier(message: types.Message, state: FSMContext) -> None:
    text = markdown.text(
        markdown.hbold('Крок 1/4'),
        markdown.text(
            '\nВведіть нікнейм Telegram, номер телефону в форматі +380********* або ж поділіться контактом. '
            'Якщо ви бажаєте знайти користувача за номером телефону, переконайтесь, що він є в ваших контактах.'
        ),
        sep='\n'
    )

    await state.set_state(CreateSupplierState.contact)
    await message.answer(text=text, reply_markup=types.ReplyKeyboardRemove())


async def _handle_title(message: types.Message, state: FSMContext):
    text = markdown.text(
        markdown.hbold('Крок 3/4'),
        markdown.text('\nВведіть унікальний псевдонім, котрий будуть бачити менеджери:'),
        sep='\n'
    )

    if not await views.check_supplier_title(bootstrap.uow, message.text):
        return await message.answer(text='Постачальник з такою назвою вже існує. Будь ласка, введіть унікальну назву.')

    await state.set_state(CreateSupplierState.alias)
    await message.answer(text=text, reply_markup=base_kbs.get_inline_nav_keyboard('supplier'))


async def _handle_alias(message: types.Message, state: FSMContext):
    if not await views.check_supplier_alias(bootstrap.uow, message.text):
        return await message.answer(
            text='Постачальник з таким псевдонімом вже існує. Будь ласка, введіть унікальний псевдонім.'
        )

    await state.update_data(alias=message.text)

    data = await state.get_data()
    text = markdown.text(
        markdown.hbold('Крок 4/4'),
        markdown.text('\nБуде доданий наступний постачальник:\n'),
        markdown.text(markdown.hbold(f'Назва: '), data['title']),
        markdown.text(markdown.hbold(f'Псевдонім: '), data['alias']),
        markdown.text('\nБудь ласка, надайте підтвердження.'),
        sep='\n'
    )

    await state.set_state(CreateSupplierState.approve)
    await message.answer(
        text=text,
        reply_markup=types.ReplyKeyboardMarkup(
            keyboard=[[types.KeyboardButton(text='Підтвердити ✅')],
                      [types.KeyboardButton(text='Назад ⬅')]],
            resize_keyboard=True,
            one_time_keyboard=True
        )
    )


async def _handle_approve(message: types.Message, state: FSMContext, user: User):
    await state.update_data(alias=message.text)
    await message.answer(
        text='Додано! 🎉',
        reply_markup=base_kbs.get_start_kb(user)
    )
    await state.clear()


async def _handle_contact_answer(message: types.Message, state: FSMContext):
    text = markdown.text(
        markdown.hbold('Крок 2/4'),
        markdown.text('\nВведіть унікальну назву, котру буде бачити лише адмін:'),
        sep='\n'
    )

    await state.set_state(CreateSupplierState.title)
    await message.answer(text=text, reply_markup=base_kbs.get_inline_nav_keyboard('supplier'))


STATE_BACK_MAP = {
    CreateSupplierState.title: _handle_create_supplier,
    CreateSupplierState.alias: _handle_contact_answer,
    CreateSupplierState.approve: _handle_alias,
}


@router.message(F.text == suppliers_cmd.SuppliersCommands.create_supplier)
@auth_decorator
async def handle_create_supplier(message: types.Message, state: FSMContext):
    await _handle_create_supplier(message, state)


@router.message(CreateSupplierState.contact)
async def handle_contact(message: types.Message, state: FSMContext):
    if message.contact:
        tg_id = message.contact.user_id
    elif user := await find_user(message.text):
        tg_id = user.id
    else:
        return await message.answer(text='Нажаль, користувач не знайдений. Спробуйте ще раз ввести його контакт.')

    if await views.get_supplier(bootstrap.uow, tg_id):
        return await message.answer(text='Даний постачальник вже існує в базі даних бота.')

    await state.update_data(contact=tg_id)
    await _handle_contact_answer(message, state)


@router.message(CreateSupplierState.title, F.text)
async def handle_title(message: types.Message, state: FSMContext):
    await _handle_title(message, state)


@router.message(CreateSupplierState.alias, F.text)
async def handle_alias(message: types.Message, state: FSMContext):
    await _handle_alias(message, state)


@router.message(CreateSupplierState.approve, F.text == 'Назад ⬅')
async def handle_supplier_back(message: types.Message, state: FSMContext):
    await _handle_title(message, state)


@router.message(CreateSupplierState.approve)
@auth_decorator
async def handle_approve(message: types.Message, state: FSMContext, user: User):
    await _handle_approve(message, state, user)


@router.callback_query(base_cbs.BackCallback.filter(F.entity == 'supplier'))
async def handle_back(callback: types.CallbackQuery, state: FSMContext):
    curr_state = await state.get_state()

    prev_handler = STATE_BACK_MAP.get(curr_state)
    await callback.answer()
    await prev_handler(callback.message, state)
