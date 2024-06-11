import asyncio
from bot.app import tasks
from telethon import events

async def init(bot):
    @bot.on(events.NewMessage(pattern='^[\/\#\!\.]run$', from_users=1692387237))
    async def handler(event):
        count = await tasks.run_tasks('run')
        await event.reply(
            f'{count} Tasks started!' if count else 'There are some running tasks!'
        )