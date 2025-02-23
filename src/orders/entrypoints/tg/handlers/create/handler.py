from aiogram import Router, F, Bot
from aiogram import types
from aiogram.fsm.context import FSMContext

from src.app.infrastructure.tg.client import send_message
from src.app.entrypoints.tg.utils import auth_decorator
from src.app.entrypoints.tg.handlers import keyboards as base_kbs
from src.suppliers.entrypoints.tg.filters import SupplierItemFilter, SupplierItemActionEnum
from src.orders.entrypoints.tg.handlers.states import CreateOrderState
from src.orders.domain.commands import CreateOrderCommand
from src.orders.bootstrap import bootstrap
from src.users import User


router = Router(name=__name__)


@router.callback_query(SupplierItemFilter.filter(F.action == SupplierItemActionEnum.create_order))
async def handle_create_order(
        callback_query: types.CallbackQuery,
        callback_data: SupplierItemFilter,
        state: FSMContext
) -> None:
    await callback_query.answer()
    await state.update_data({CreateOrderState.create_order_supplier_tg_id: callback_data.tg_id})
    await state.set_state(CreateOrderState.waiting_order_content)

    await callback_query.bot.send_message(
        chat_id=callback_query.from_user.id,
        text='Будь ласка, сформуйте замовлення. '
             'Ви повинні додати текст, а також можете прикріпити файл чи фото. '
             'Далі від вас потрібно буде підтвердження.'
    )


@router.message(CreateOrderState.waiting_order_content, F.text)
async def handle_content(message: types.Message, state: FSMContext) -> None:
    await state.update_data({
        CreateOrderState.create_order_chat_id: message.chat.id,
        CreateOrderState.create_order_bot_message_id: message.message_id
    })

    await state.set_state(CreateOrderState.waiting_approve)

    await message.answer(
        text='Ваше замовлення майже готово. Будь ласка, надайте підтвердження.',
        reply_markup=types.ReplyKeyboardMarkup(
            keyboard=[[types.KeyboardButton(text='Підтвердити ✅')],
                      [types.KeyboardButton(text='Скасувати ❌')]],
            resize_keyboard=True,
            one_time_keyboard=True
        )
    )


@router.message(CreateOrderState.waiting_approve, F.text == 'Підтвердити ✅')
@auth_decorator
async def handle_approve(message: types.Message, state: FSMContext, bot: Bot, user: User) -> None:
    data = await state.get_data()

    supplier_tg_id = data[CreateOrderState.create_order_supplier_tg_id]
    bot_message_id = data[CreateOrderState.create_order_bot_message_id]
    chat_id = data[CreateOrderState.create_order_chat_id]

    bot_msg = await bot.forward_message(
        from_chat_id=chat_id,
        chat_id=chat_id,
        message_id=bot_message_id
    )

    await state.clear()
    msg = await send_message(supplier_tg_id, bot_msg.text)

    cmd = CreateOrderCommand(
        supplier_tg_id=supplier_tg_id,
        user_tg_id=message.from_user.id,
        message_id=msg.id,
        text=bot_msg.text
    )

    await bootstrap.handle(cmd)

    await message.answer(
        text='Замовлення успішно створено і відправлено постачальнику! 🎉',
        reply_markup=base_kbs.get_start_kb(user)
    )


@router.message(CreateOrderState.waiting_approve, F.text == 'Скасувати ❌')
@auth_decorator
async def handle_reject(message: types.Message, state: FSMContext, user: User) -> None:
    await state.clear()
    await message.answer(
        text='Замовлення скасовано ❌',
        reply_markup=base_kbs.get_start_kb(user)
    )
