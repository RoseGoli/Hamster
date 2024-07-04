import asyncio
from telethon import events
from src.config import settings

async def init(bot):
    @bot.on(events.NewMessage(pattern=r'Shutdown🔥', func=lambda e: e.is_private, from_users=settings.OWNERS))
    async def handler(event):
        loop      = asyncio.get_event_loop()
        all_tasks = asyncio.all_tasks(loop=loop)
        tasks     = [
            task for task in all_tasks
            if isinstance(task, asyncio.Task) and task._coro.__name__ == 'run'
        ]

        for task in tasks:
            try:
                task.cancel()
            except:
                ...

        await event.respond('<b>Shutted Down !</b>')
        bot.disconnect()