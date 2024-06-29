from telethon import events
from src.config import settings
from src.utils.helpers import rtl, align, format_large_num
from src.database.hamster import hamster

async def init(bot):
    @bot.on(events.NewMessage(pattern='Total Coins 🗼', from_users=settings.OWNERS))
    async def handler(event):
        total    = hamster.total_info()
        thamster = align({
            '💰 Total Balance' : f"<b>{format_large_num(int(total['balance']))}</b>",
            '📊 Total PPH'     : f"<b>{format_large_num(int(total['profit']))}</b>"
        })
        await event.reply(f"<b>🐹 Hamster:</b>\n{thamster}")