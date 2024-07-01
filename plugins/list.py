from telethon import events
from src.config import settings
from src.utils.helpers import rtl
from src.utils.scripts import chunk
from telethon.tl.custom.button import Button
from src.database.acc import accounts

async def init(bot):
    @bot.on(events.NewMessage(pattern='📊 Accounts List 📊', from_users=settings.OWNERS))
    @bot.on(events.CallbackQuery(data='list', chats=settings.OWNERS))
    async def handler(event):
        list   = [Button.inline(x['name'], f"user-{x['user_id']}") for x in accounts.select().dicts()]
        method = 'reply' if getattr(event, 'text', False) else 'edit'

        if list:
            msg = "<b>🌱 Your account list :\n</b>"
        else:
            msg = "<b>📦 You dont have any accounts!\n</b>"

        await getattr(event, method)(rtl(msg), buttons = [x for x in chunk(list, 3)] if list else None)