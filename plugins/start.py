from telethon import events
from src.config import settings
from telethon.tl.custom.button import Button

async def init(bot):
    @bot.on(events.NewMessage(pattern=r'^[\/\#\!\.]start$', func=lambda e: e.is_private, from_users=settings.OWNERS))
    async def handler(event):
        user = await event.get_sender()
        await event.reply(f'Hey <b>{user.first_name}</b>!', buttons = [
            [Button.text('📊 Accounts List 📊', resize = True)],
            [Button.text('🚏 Clickers Status'), Button.text('Total Coins 🗼')],
            [Button.text('🔄 Restart Bot'), Button.text('Shutdown🔥')],
            [Button.text('🎛 Resources 🎛')]
        ])