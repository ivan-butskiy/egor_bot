from aiogram import Router, F
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown

from src.app.infrastructure.tg.client import find_user
from src.app.entrypoints.tg.utils import auth_decorator
from src.app.entrypoints.tg.handlers import keyboards as base_kbs
from src.users import User
from src.suppliers import views
from src.suppliers.domain.commands import UpdateSupplier
from src.suppliers.bootstrap import bootstrap
from src.suppliers.entrypoints.tg.filters import SupplierItemFilter, SupplierItemActionEnum
from src.suppliers.entrypoints.tg.handlers.states import UpdateSupplierState
from .keyboards import get_edit_supplier_kb
from .filters import EditSupplierFilter, EditSupplierActionsEnum


router = Router(name=__name__)


@router.callback_query(SupplierItemFilter.filter(F.action == SupplierItemActionEnum.edit))
async def handle_edit_supplier(
        callback_query: types.CallbackQuery,
        callback_data: SupplierItemFilter,
        state: FSMContext
) -> None:
    await state.update_data(update_tg_id=callback_data.tg_id)
    await state.set_state(UpdateSupplierState.update_tg_id)

    text = markdown.text(
        'Будь ласка, оберіть, що ви хочете змінити для постачальника:'
    )

    await callback_query.answer()
    await callback_query.bot.send_message(
        chat_id=callback_query.from_user.id,
        text=text,
        reply_markup=get_edit_supplier_kb(callback_data.tg_id)
    )


@router.callback_query(EditSupplierFilter.filter(F.action == EditSupplierActionsEnum.contact))
async def set_contact_state(
        callback_query: types.CallbackQuery,
        state: FSMContext
) -> None:
    await callback_query.answer()
    await state.set_state(UpdateSupplierState.update_contact)
    text = markdown.text(
        '\nВведіть нікнейм Telegram, номер телефону в форматі +380********* або ж поділіться контактом. '
        'Якщо ви бажаєте знайти користувача за номером телефону, переконайтесь, що він є в ваших контактах.'
    )
    await callback_query.bot.send_message(
        chat_id=callback_query.from_user.id,
        text=text
    )


@router.callback_query(EditSupplierFilter.filter(F.action == EditSupplierActionsEnum.title))
async def set_title_state(
        callback_query: types.CallbackQuery,
        state: FSMContext
) -> None:
    await callback_query.answer()
    await state.set_state(UpdateSupplierState.update_title)
    await callback_query.bot.send_message(
        chat_id=callback_query.from_user.id,
        text='Введіть унікальну назву, котру буде бачити лише адмін:'
    )


@router.callback_query(EditSupplierFilter.filter(F.action == EditSupplierActionsEnum.alias))
async def set_alias_state(
        callback_query: types.CallbackQuery,
        state: FSMContext
) -> None:
    await callback_query.answer()
    await state.set_state(UpdateSupplierState.update_title)
    await callback_query.bot.send_message(
        chat_id=callback_query.from_user.id,
        text='Введіть унікальний псевдонім, котрий будуть бачити менеджери:'
    )


@router.callback_query(EditSupplierFilter.filter(F.action == EditSupplierActionsEnum.cancel))
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


@router.message(UpdateSupplierState.update_contact)
async def handle_contact(message: types.Message, state: FSMContext):
    if message.contact:
        tg_id = message.contact.user_id
    elif user := await find_user(message.text):
        tg_id = user.id
    else:
        return await message.answer(text='Нажаль, користувач не знайдений. Спробуйте ще раз ввести його контакт.')

    data = await state.get_data()
    current_tg_id = data['update_tg_id']

    if await views.get_supplier(bootstrap.uow, tg_id, current_tg_id):
        return await message.answer(text='Даний постачальник вже існує в базі даних бота.')

    await state.clear()

    cmd = UpdateSupplier(
        tg_id=current_tg_id,
        new_tg_id=tg_id
    )

    await bootstrap.handle(cmd)

    text = markdown.text(
        markdown.hbold('Контакт постачальника успішно редаговано!\n'),
        markdown.text('Оберіть, що б ви ще хотіли редагувати:'),
        sep='\n'
    )

    await message.answer(
        text=text,
        reply_markup=get_edit_supplier_kb(tg_id)
    )


@router.message(UpdateSupplierState.update_title)
async def handle_title(message: types.Message, state: FSMContext):
    data = await state.get_data()
    current_tg_id = data['update_tg_id']
    if not await views.check_supplier_title(bootstrap.uow, message.text, current_tg_id):
        return await message.answer(text='Постачальник з такою назвою вже існує. Будь ласка, введіть унікальну назву.')

    cmd = UpdateSupplier(
        tg_id=current_tg_id,
        title=message.text
    )

    await bootstrap.handle(cmd)

    text = markdown.text(
        markdown.hbold('Назва постачальника успішно редагована!\n'),
        markdown.text('Оберіть, що б ви ще хотіли редагувати:'),
        sep='\n'
    )

    await message.answer(
        text=text,
        reply_markup=get_edit_supplier_kb(current_tg_id)
    )


@router.message(UpdateSupplierState.update_title)
async def handle_alias(message: types.Message, state: FSMContext):
    data = await state.get_data()
    current_tg_id = data['update_tg_id']
    if not await views.check_supplier_alias(bootstrap.uow, message.text, current_tg_id):
        return await message.answer(
            text='Постачальник з таким псевдонімом вже існує. Будь ласка, введіть унікальний псевдонім.'
        )

    cmd = UpdateSupplier(
        tg_id=current_tg_id,
        alias=message.text
    )

    await bootstrap.handle(cmd)

    text = markdown.text(
        markdown.hbold('Псевдонім постачальника успішно редаговано!\n'),
        markdown.text('Оберіть, що б ви ще хотіли редагувати:'),
        sep='\n'
    )

    await message.answer(
        text=text,
        reply_markup=get_edit_supplier_kb(current_tg_id)
    )
