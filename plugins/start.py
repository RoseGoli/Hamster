from telethon import events
from src.config import settings
from telethon.tl.custom.button import Button

async def init(bot):
    @bot.on(events.NewMessage(pattern='^[\/\#\!\.]start$', from_users=settings.OWNERS))
    async def handler(event):
        user = await event.get_sender()
        await event.reply(f'Hey <b>{user.first_name}</b>!', buttons = [
            [Button.text('📊 Accounts List 📊', resize = True)],
            [Button.text('روشن کردن ربات'), Button.text('خاموش کردن ربات')]
        ])