from bot.app import TaskRunner
from telethon import events
from bot.config import settings

import numpy as np


async def init(bot):
    @bot.on(events.NewMessage(pattern='^[\/\#\!\.]urls$', from_users=settings.ADMIN_ID))
    async def handler(event):
        await event.reply('Working on it...')
        tasks = TaskRunner()
        urls  = await tasks.run_tasks('get_web_data', return_results=True, only_url=True)
        links = [f'<a href="{url}">Webapp {i+1}</a>' for i, url in enumerate(urls)]
        links = np.array_split(links, 5)

        await tasks.cancel_all_tasks()
        for link in links:
            await event.reply("\n".join(link))