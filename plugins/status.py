from telethon import events
from src.config import settings
from src.database.config import conf
from src.utils.helpers import rtl, emoticate, camel2space
from telethon.tl.custom.button import Button

async def init(bot):
    @bot.on(events.NewMessage(pattern=r'^🚏 Clickers Settings$', func=lambda e: e.is_private, from_users=settings.OWNERS))
    async def handler(event):
        info = conf.fetch()
        del info['id']

        msg  = "<b>Change bot clickers status:\n</b>"
        list = [
            [
                Button.inline(camel2space(key.replace('hamsterKombat', '🐹')), f"change-{key}"),
                Button.inline(emoticate(value), f"change-{key}")
            ]
            for key, value in info.items()
        ]

        await event.reply(rtl(msg), buttons = list)

    @bot.on(events.CallbackQuery(pattern='^change\-(.*)$', chats=settings.OWNERS))
    async def handler(event):
        index = event.pattern_match.group(1).decode('utf-8')
        info  = conf.fetch(index)

        conf.insertOrUpdateConfig(**{index: not info})

        info = conf.fetch()
        del info['id']
        
        msg  = "<b>Change bot clickers status:\n</b>"
        list = [
            [
                Button.inline(camel2space(key.replace('hamsterKombat', '🐹')), f"change-{key}"),
                Button.inline(emoticate(value), f"change-{key}")
            ]
            for key, value in info.items()
        ]

        await event.edit(rtl(msg), buttons = list)