import asyncio
from bot.app import tasks
from telethon import events
from bot.config import settings

async def init(bot):
    @bot.on(events.NewMessage(pattern='^[\/\#\!\.]run$', from_users=settings.ADMIN_ID))
    async def handler(event):
        count = await tasks.run_tasks('run')
        await event.reply(
            f'{count} Tasks started!' if count else 'There are some running tasks!'
        )