from telethon import events
from src.config import settings
from src.database.hamster import hamster
from src.utils.helpers import align, format_large_num

async def init(bot):
    @bot.on(events.NewMessage(pattern='Total Coins 🗼', func=lambda e: e.is_private, from_users=settings.OWNERS))
    async def handler(event):
        total    = hamster.total_info()
        thamster = align({
            '💰 Total Balance' : f"<b>{format_large_num(int(total['balance']))}</b>",
            '📊 Total PPH'     : f"<b>{format_large_num(int(total['profit']))}</b>"
        })
        await event.reply(f"<b>🐹 Hamster:</b>\n{thamster}")