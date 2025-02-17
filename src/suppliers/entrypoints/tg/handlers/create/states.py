from aiogram.fsm.state import StatesGroup, State


class CreateSupplierState(StatesGroup):
    contact = State()
    title = State()
    alias = State()
    approve = State()
