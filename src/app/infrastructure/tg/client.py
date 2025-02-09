import os

from telethon import TelegramClient


API_ID = int(os.getenv('TG_API_ID'))
API_HASH = os.getenv('TG_API_HASH')
SESSION_NAME = f'{os.getcwd()}/telethon'

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
