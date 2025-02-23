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
from src.suppliers.domain.commands import CreateSupplierCommand
from src.suppliers.entrypoints.tg.handlers.states import CreateSupplierState


router = Router(name=__name__)


async def get_create_supplier_response(message: types.Message, state: FSMContext) -> None:
    text = markdown.text(
        markdown.hbold('Крок 1/4'),
        markdown.text(
            '\nВведіть нікнейм Telegram, номер телефону в форматі +380********* або ж поділіться контактом. '
            'Якщо ви бажаєте знайти користувача за номером телефону, переконайтесь, що він є в ваших контактах.'
        ),
        sep='\n'
    )

    await state.set_state(CreateSupplierState.create_supplier_contact)
    await message.answer(text=text, reply_markup=types.ReplyKeyboardRemove())


async def get_contact_response(message: types.Message, state: FSMContext):
    text = markdown.text(
        markdown.hbold('Крок 2/4'),
        markdown.text('\nВведіть унікальну назву, котру буде бачити лише адмін:'),
        sep='\n'
    )

    await state.set_state(CreateSupplierState.create_supplier_title)
    await message.answer(text=text, reply_markup=base_kbs.get_inline_nav_keyboard('supplier'))


async def get_title_response(message: types.Message, state: FSMContext):
    text = markdown.text(
        markdown.hbold('Крок 3/4'),
        markdown.text('\nВведіть унікальний псевдонім, котрий будуть бачити менеджери:'),
        sep='\n'
    )
    await state.set_state(CreateSupplierState.create_supplier_alias)
    await message.answer(text=text, reply_markup=base_kbs.get_inline_nav_keyboard('supplier'))


async def get_alias_response(message: types.Message, state: FSMContext):
    data = await state.get_data()
    text = markdown.text(
        markdown.hbold('Крок 4/4'),
        markdown.text('\nБуде доданий наступний постачальник:\n'),
        markdown.text(markdown.hbold(f'Назва: '), data['create_supplier_title']),
        markdown.text(markdown.hbold(f'Псевдонім: '), data['create_supplier_alias']),
        markdown.text('\nБудь ласка, надайте підтвердження.'),
        sep='\n'
    )

    await state.set_state(CreateSupplierState.create_supplier_approve)
    await message.answer(
        text=text,
        reply_markup=types.ReplyKeyboardMarkup(
            keyboard=[[types.KeyboardButton(text='Підтвердити ✅')],
                      [types.KeyboardButton(text='Назад ⬅')]],
            resize_keyboard=True,
            one_time_keyboard=True
        )
    )


@router.message(F.text == suppliers_cmd.SuppliersCommands.create_supplier)
async def handle_create_supplier(message: types.Message, state: FSMContext):
    await get_create_supplier_response(message, state)


@router.message(CreateSupplierState.create_supplier_contact)
async def handle_contact(message: types.Message, state: FSMContext):
    if message.contact:
        tg_id = message.contact.user_id
    elif user := await find_user(message.text):
        tg_id = user.id
    else:
        return await message.answer(text='Нажаль, користувач не знайдений. Спробуйте ще раз ввести його контакт.')

    if await views.get_supplier(bootstrap.uow, tg_id):
        return await message.answer(text='Даний постачальник вже існує в базі даних бота.')

    await state.update_data(create_supplier_contact=tg_id)
    await get_contact_response(message, state)


@router.message(CreateSupplierState.create_supplier_title, F.text)
async def handle_title(message: types.Message, state: FSMContext):
    if not await views.check_supplier_title(bootstrap.uow, message.text):
        return await message.answer(text='Постачальник з такою назвою вже існує. Будь ласка, введіть унікальну назву.')
    await state.update_data(create_supplier_title=message.text)
    await get_title_response(message, state)


@router.message(CreateSupplierState.create_supplier_alias, F.text)
async def handle_alias(message: types.Message, state: FSMContext):
    if not await views.check_supplier_alias(bootstrap.uow, message.text):
        return await message.answer(
            text='Постачальник з таким псевдонімом вже існує. Будь ласка, введіть унікальний псевдонім.'
        )

    await state.update_data(create_supplier_alias=message.text)
    await get_alias_response(message, state)


@router.message(CreateSupplierState.create_supplier_approve, F.text == 'Назад ⬅')
async def handle_supplier_back(message: types.Message, state: FSMContext):
    await get_title_response(message, state)


@router.message(CreateSupplierState.create_supplier_approve, F.text == 'Підтвердити ✅')
@auth_decorator
async def handle_approve(message: types.Message, state: FSMContext, user: User):
    data: dict = await state.get_data()
    cmd = CreateSupplierCommand(
        tg_id=data['create_supplier_contact'],
        title=data['create_supplier_title'],
        alias=data['create_supplier_alias']
    )
    await state.clear()
    await bootstrap.handle(cmd)
    await message.answer(
        text='Додано! 🎉',
        reply_markup=base_kbs.get_start_kb(user)
    )


@router.callback_query(base_cbs.BackCallback.filter(F.entity == 'supplier'))
async def handle_back(callback: types.CallbackQuery, state: FSMContext):
    curr_state = await state.get_state()

    prev_handler = _STATE_BACK_MAP.get(curr_state)
    await callback.answer()
    await prev_handler(callback.message, state)


_STATE_BACK_MAP = {
    CreateSupplierState.create_supplier_title: get_create_supplier_response,
    CreateSupplierState.create_supplier_alias: get_contact_response,
    CreateSupplierState.create_supplier_approve: get_title_response,
}
