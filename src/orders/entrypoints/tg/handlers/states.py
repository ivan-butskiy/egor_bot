from aiogram.fsm.state import StatesGroup, State


class CreateOrderState(StatesGroup):
    create_order_supplier_tg_id = State()
    waiting_order_content = State()
    create_order_chat_id = State()
    create_order_bot_message_id = State()
    waiting_approve = State()
