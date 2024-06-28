import json

from telethon import events
from src.config import settings
from src.database.acc import acc
from telethon.tl.custom.button import Button

async def init(bot):
    @bot.on(events.CallbackQuery(pattern='^user\-(\d+)$', chats=settings.OWNERS))
    async def handler(event):
        id   = int(event.pattern_match.group(1))
        info = acc.fetch(id)

        await event.edit(text = json.dumps(info, indent=4), buttons = Button.inline('back', 'list'))