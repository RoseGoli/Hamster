from telethon import events
from bot.config import settings

async def init(bot):
    @bot.on(events.NewMessage(pattern='^[\/\#\!\.]start$', from_users=settings.ADMIN_ID))
    async def handler(event):
        user = await event.get_sender()
        await event.reply(f'Hey <b>{user.first_name}</b>!')