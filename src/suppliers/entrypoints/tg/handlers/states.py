from aiogram.fsm.state import StatesGroup, State


class CreateSupplierState(StatesGroup):
    create_contact = State()
    create_title = State()
    create_alias = State()
    create_approve = State()


class UpdateSupplierState(StatesGroup):
    update_tg_id = State()
    update_contact = State()
    update_title = State()
    update_alias = State()
