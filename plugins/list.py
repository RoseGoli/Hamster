from telethon import events
from src.config import settings
from src.utils.scripts import chunk
from telethon.tl.custom.button import Button
from src.database.acc import accounts

async def init(bot):
    @bot.on(events.NewMessage(pattern='^[\/\#\!\.]list$', from_users=settings.OWNERS))
    async def handler(event):
        list = [Button.inline(x['name'], f"user-{x['user_id']}") for x in accounts.select().dicts()]
        await event.reply('list', buttons = [x for x in chunk(list, 3)] if list else None)

    @bot.on(events.CallbackQuery(data='list', chats=settings.OWNERS))
    async def handler(event):
        list = [Button.inline(x['name'], f"user-{x['user_id']}") for x in accounts.select().dicts()]
        await event.edit('list', buttons = [x for x in chunk(list, 3)] if list else None)