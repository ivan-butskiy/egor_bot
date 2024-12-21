import asyncio
import logging
import sys

from src.bot import dispatcher, bot
from src.bot.router import setup_routers


async def main() -> None:
    setup_routers(dispatcher)
    await dispatcher.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
