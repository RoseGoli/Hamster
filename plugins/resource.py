from telethon import events
from src.config import settings
from src.utils.helpers import align, get_server_usage

async def init(bot):
    @bot.on(events.NewMessage(pattern='🎛 Resources 🎛', func=lambda e: e.is_private, from_users=settings.OWNERS))
    async def handler(event):
        su = get_server_usage()

        mem_usage   = su['memory_usage_MB']
        mem_total   = su['memory_total_MB']
        mem_percent = su['memory_percent']
        cpu_percent = su['cpu_percent']

        msg = align({
            '🧠 CPU usage'      : f"<b>{cpu_percent:.2f}%</b>",
            '💯 Memory Percent' : f"<b>{mem_percent:.2f}%</b>",
            '🫀 Memory usage'   : f"<code>{mem_usage:.2f}/{mem_total:.2f} MB</code>"
        })

        await event.reply(msg)