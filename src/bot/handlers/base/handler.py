from aiogram import Router
from aiogram import html
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from src.domain.users import User
from src.bot.handlers.utils import auth_decorator
from . import keyboards as kb


base_router = Router()


@base_router.message(CommandStart())
@auth_decorator
async def handle_start(message: Message, user: User) -> None:
    """
    This handler receives messages with /start` command
    """
    await message.answer(
        f'Привіт, {html.bold(message.from_user.full_name)}! '
        f'Оберіть необхідну дію:',
        reply_markup=kb.get_start_keyboard(user),
    )


@base_router.message(Command('help'))
@auth_decorator
async def handle_help(message: Message) -> None:
    text = ('За допомогою цього чат-бота ви зможете оформлювати '
            'замовлення постачальникам ТД Петровський.')
    await message.answer(text=text)
