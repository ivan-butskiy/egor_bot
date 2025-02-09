from aiogram import Router, F
from aiogram import html
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from src.users import User
from src.app.entrypoints.tg.utils import auth_decorator
from src.app.entrypoints.tg.handlers import commands as cmd, keyboards as kb

router = Router(name=__name__)


@router.message(CommandStart())
@router.message(F.text == cmd.StartKbCommands.to_the_head)
@auth_decorator
async def handle_start(message: Message, user: User) -> None:
    """
    This handler receives messages with /start` command
    """
    await message.answer(
        f'Привіт, {html.bold(message.from_user.full_name)}! '
        f'Оберіть необхідну дію:',
        reply_markup=kb.get_start_kb(user),
    )


@router.message(Command('help'))
@auth_decorator
async def handle_help(message: Message) -> None:
    text = ('За допомогою цього чат-бота ви зможете оформлювати '
            'замовлення постачальникам ТД Петровський.')
    await message.answer(text=text)
