import json

from telethon import events
from src.config import settings
from src.database.acc import acc
from telethon.tl.custom.button import Button

def align(data):
    max_key_length = max(len(str(key)) for key in data.keys())
    result         = []

    for key, value in data.items():
        result.append(f"<code>{str(key).ljust(max_key_length)} </code>: {value}")

    return "\n".join(result)

async def init(bot):
    @bot.on(events.CallbackQuery(pattern='^user\-(\d+)$', chats=settings.OWNERS))
    async def handler(event):
        id   = int(event.pattern_match.group(1))
        info = acc.fetch(id)

        text = align({
            "🌟<b>نام</b>" : f"{info['name']}",
            "💡<b>آیدی عددی</b>" : f"<code>{info['user_id']}</code>",
            "👤<b>یوزرنیم</b>" : f"@{info['username']}",
            "📞<b>شماره تلفن</b>" : f"@{info['phone_number']}",
            "💰<b>موجودی</b>" : f"{info['balance']}",
            "📈<b>سود</b>" : f"{info['profit']}",
            "🕒<b>آخرین ورود</b>" : f"{info['last_login']}",
        })

        await event.edit(text = text + "\n.", buttons = Button.inline('back', 'list'))