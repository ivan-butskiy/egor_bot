from aiogram import Router
from aiogram import html
from aiogram.filters import CommandStart
from aiogram.types import Message


base_router = Router()


@base_router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer(
        f'Привіт, {html.bold(message.from_user.full_name)}! '
        f'Оберіть необхідну дію:',
    )
