from aiogram import Router, F
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown

from src.app.infrastructure.tg.client import find_user
from src.app.entrypoints.tg.handlers import keyboards as base_kbs
from src.app.entrypoints.tg.utils import auth_decorator
from src.users import views
from src.users.bootstrap import bootstrap
from src.users.entrypoints.tg import commands as users_cmd
from src.users.domain.commands import CreateUserCommand
from src.users.domain.model import User, UserTypeEnum
from src.users.entrypoints.tg.handlers.states import CreateUserState


router = Router(name=__name__)


@router.message(F.text == users_cmd.UsersCommand.create_user)
@router.message(CreateUserState.create_user_approve, F.text == 'Назад ⬅')
async def handle_create_user(message: types.Message, state: FSMContext):
    text = markdown.text(
        'Введіть нікнейм Telegram, номер телефону в форматі +380********* або ж поділіться контактом. '
        'Якщо ви бажаєте знайти користувача за номером телефону, переконайтесь, що він є в ваших контактах.'
    )

    await state.set_state(CreateUserState.create_user_contact)
    await message.answer(text=text, reply_markup=types.ReplyKeyboardRemove())


@router.message(CreateUserState.create_user_contact)
async def handle_contact(message: types.Message, state: FSMContext):
    entity: types.Contact | types.User

    if message.contact:
        tg_id = message.contact.user_id
        entity = message.contact
    elif entity := await find_user(message.text):
        tg_id = entity.id
    else:
        return await message.answer(text='Нажаль, користувач не знайдений. Спробуйте ще раз ввести його контакт.')

    if await views.get_user(bootstrap.uow, tg_id):
        return await message.answer(text='Даний користувач вже існує в базі даних бота.')

    await state.update_data({
        CreateUserState.create_user_contact: tg_id,
        CreateUserState.create_user_first_name: entity.first_name,
        CreateUserState.create_user_last_name: entity.last_name,
    })

    await state.set_state(CreateUserState.create_user_approve)

    text = markdown.text(
        markdown.text('Знайдено наступного користувача:'),
        markdown.text(f"Ім'я - {entity.first_name}"),
        markdown.text(f"Прізвище - {entity.last_name or ''}\n"),
        markdown.text(f"Ім'я та прізвище ви зможете згодом відредагувати. "
                      f"Будь ласка, надайте підтвердження."),
        sep='\n'
    )

    await message.answer(
        text=text,
        reply_markup=types.ReplyKeyboardMarkup(
            keyboard=[[types.KeyboardButton(text='Підтвердити ✅')],
                      [types.KeyboardButton(text='Назад ⬅')]],
            resize_keyboard=True,
            one_time_keyboard=True
        )
    )


@router.message(CreateUserState.create_user_approve, F.text == 'Підтвердити ✅')
@auth_decorator
async def handle_approve(message: types.Message, state: FSMContext, user: User):
    data: dict = await state.get_data()
    cmd = CreateUserCommand(
        tg_id=data[CreateUserState.create_user_contact],
        first_name=data[CreateUserState.create_user_first_name],
        last_name=data[CreateUserState.create_user_last_name],
        type=UserTypeEnum.manager
    )
    await state.clear()
    await bootstrap.handle(cmd)
    await message.answer(
        text='Додано! 🎉',
        reply_markup=base_kbs.get_start_kb(user)
    )
