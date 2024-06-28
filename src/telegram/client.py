import os
from src.config import settings
from telethon import TelegramClient

bot = TelegramClient(
    os.path.join(settings.SESSION_PATH, settings.MAIN_NAME),
    settings.API_ID,
    settings.API_HASH
)

async def startClient():
    await bot.start(bot_token=settings.TG_TOKEN)

async def stopClient():
    await bot.disconnect()

async def getClient():
    return bot