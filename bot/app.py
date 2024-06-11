from bot.config import settings
from telethon import TelegramClient
from bot.utils.launcher import TaskRunner


tasks = TaskRunner()
bot   = TelegramClient(
    'bot',
    settings.API_ID,
    settings.API_HASH
)

async def startClient():
    await bot.start()

async def stopClient():
    await bot.disconnect()

async def getClient():
    return bot