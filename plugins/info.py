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

        text = align({
            "🌟 Name"       : f"<b>{info['name']}</b>",
            "🫀 UserId"     : f"<code>{info['user_id']}</code>",
            #"👤 Username"   : f"@{info['username']}",
            "📞 Phone"      : f"@{info['phone_number']}",
            "💰 Balance"    : f"{info['balance']}",
            "📈 PPH"        : f"{info['profit']}",
            "🕒 Last Login" : datetime.fromtimestamp(info['last_login'])
        })

        await event.edit(text, buttons = Button.inline('back', 'list'))