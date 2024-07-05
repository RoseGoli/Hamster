from telethon import events
from src.config import settings
from src.database.config import conf
from src.utils.helpers import rtl, emoticate
from telethon.tl.custom.button import Button

async def init(bot):
    @bot.on(events.NewMessage(pattern=r'^🚏 Clickers Settings$', func=lambda e: e.is_private, from_users=settings.OWNERS))
    async def handler(event):
        info = conf.fetch()
        del info['id']

        msg  = "<b>Change bot clickers status:\n</b>"
        list = [
            [Button.inline(key, f"change-{key}"), Button.inline(emoticate(value), f"change-{key}")]
            for key, value in info.items()
        ]

        await event.reply(rtl(msg), buttons = list)

    @bot.on(events.CallbackQuery(pattern='^change\-(.*)$', chats=settings.OWNERS))
    async def handler(event):
        index = event.pattern_match.group(1).decode('utf-8')
        info  = conf.fetch()

        del info['id']
        conf.insertOrUpdateConfig(**{index: not info[index]})

        msg  = "<b>Change bot clickers status:\n</b>"
        list = [
            [Button.inline(key, f"change-{key}"), Button.inline(emoticate(not value), f"change-{key}")]
            for key, value in info.items()
        ]

        await event.edit(rtl(msg), buttons = list)