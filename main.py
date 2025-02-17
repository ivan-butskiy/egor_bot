import sys
import asyncio
import logging

from src.app.infrastructure.tg.bot import dispatcher, bot


async def main():
    await dispatcher.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
