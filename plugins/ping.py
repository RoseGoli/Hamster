import time
import asyncio

from telethon import events

async def init(bot):
    @bot.on(events.NewMessage(pattern='^[\/\#\!\.]ping$', func=lambda e: e.is_private, forwards=False, outgoing=False))
    async def handler(event):
        s = time.time()
        message = await event.reply('Pong!')
        d = time.time() - s
        await message.edit(f'Pong! <i>(reply took {d:.2f}s)</i>')
        await asyncio.sleep(5)
        await asyncio.gather(event.delete(), message.delete())