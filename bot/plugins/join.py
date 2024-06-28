from bot.app import TaskRunner
from telethon import events
from bot.config import settings

async def init(bot):
    @bot.on(events.NewMessage(pattern='^[\/\#\!\.]join\s(.*)$', from_users=settings.ADMIN_ID))
    async def handler(event):
        chanl = event.text.split(" ")[1]
        msg   = await event.reply('Working on it...')
        tasks = TaskRunner()
        joins = await tasks.run_tasks('join_channel', return_results=True, channel=chanl)

        await tasks.cancel_all_tasks()
        await msg.edit(f"{sum(1 for join in joins if join)} users join the channel of {chanl}")
        