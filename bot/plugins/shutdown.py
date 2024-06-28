from telethon import events
from bot.config import settings

async def init(bot):
    @bot.on(events.NewMessage(pattern='^[\/\#\!\.]shut$', from_users=settings.ADMIN_ID))
    async def handler(event):
        await event.respond('<b>Shutted Down !</b>')
        bot.disconnect()