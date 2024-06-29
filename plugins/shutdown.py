from telethon import events
from src.config import settings

async def init(bot):
    @bot.on(events.NewMessage(pattern='Shutdown🔥', from_users=settings.OWNERS))
    async def handler(event):
        await event.respond('<b>Shutted Down !</b>')
        bot.disconnect()