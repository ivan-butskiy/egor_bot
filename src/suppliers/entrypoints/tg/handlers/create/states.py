from aiogram.fsm.state import StatesGroup, State


class UserState(StatesGroup):
    username = State()
    title = State()
    alias = State()
