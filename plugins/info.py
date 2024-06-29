from telethon import events
from datetime import datetime
from src.config import settings
from src.database.acc import acc
from src.utils.helpers import align
from telethon.tl.custom.button import Button

async def init(bot):
    @bot.on(events.CallbackQuery(pattern='^user\-(\d+)$', chats=settings.OWNERS))
    async def handler(event):
        id   = int(event.pattern_match.group(1))
        info = acc.fetch(id)

        main = align({
            "🌟 Name"       : f"<b>{info['name']}</b>",
            "🫀 UserId"     : f"<code>{info['user_id']}</code>",
            "👤 Username"   : f"@{info['username']}",
            "📞 Phone"      : f"@{info['phone_number']}"
        })

        hamster = align({
            "💰 Balance"    : f"{info['hamsterKombat']['balance']}",
            "📈 PPH"        : f"{info['hamsterKombat']['profit']}",
            "🕒 Last Login" : datetime.fromtimestamp(info['hamsterKombat']['last_login'])
        })
        
        keys = [
            [Button.url('🐹 Hamster', info['hamsterKombat']['url'])],
            [Button.inline('back', 'list')]
        ]

        await event.edit(f"<b>👳🏿‍♂️ Account:</b>\n{main}\n<b>🐹 Hamster:</b>\n{hamster}", buttons = keys)