from telethon import events
from bot.app import tasks

async def init(bot):
    @bot.on(events.NewMessage(pattern='^[\/\#\!\.]stop$', from_users=1692387237))
    async def handler(event):
        count = await tasks.cancel_all_tasks()
        await event.reply(
            f'{count} Tasks canceled!' if count else 'There are no tasks to cancel!'
        )