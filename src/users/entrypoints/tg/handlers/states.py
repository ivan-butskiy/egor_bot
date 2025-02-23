from aiogram.fsm.state import StatesGroup, State


class CreateUserState(StatesGroup):
    create_user_contact = State()
    create_user_first_name = State()
    create_user_last_name = State()
    create_user_approve = State()


class UpdateUserState(StatesGroup):
    update_user_tg_id = State()
    update_user_first_name = State()
    update_user_last_name = State()
