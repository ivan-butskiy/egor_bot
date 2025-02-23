from aiogram.fsm.state import StatesGroup, State


class CreateSupplierState(StatesGroup):
    create_supplier_contact = State()
    create_supplier_title = State()
    create_supplier_alias = State()
    create_supplier_approve = State()


class UpdateSupplierState(StatesGroup):
    update_supplier_tg_id = State()
    update_supplier_contact = State()
    update_supplier_title = State()
    update_supplier_alias = State()
