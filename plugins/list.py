from telethon import events
from src.config import settings
from src.utils.scripts import chunk
from telethon.tl.custom.button import Button
from src.database.acc import accounts

async def init(bot):
    @bot.on(events.NewMessage(pattern='📊 لیست اکانت ها 📊', from_users=settings.OWNERS))
    @bot.on(events.CallbackQuery(data='list', chats=settings.OWNERS))
    async def handler(event):
        list   = [Button.inline(x['name'], f"user-{x['user_id']}") for x in accounts.select().dicts()]
        msg    = '🌱 لیست اکانت های شما :' if list else '📦 متاسفانه اکانت فعالی نداریم!'
        method = 'reply' if getattr(event, 'text', False) else 'edit'

        await getattr(event, method)(msg, buttons = [x for x in chunk(list, 3)] if list else None)