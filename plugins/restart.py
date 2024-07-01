import os
import sys

from telethon import events
from src.config import settings

MAGIC_FILE = os.path.join(os.path.dirname(__file__), 'self-update.lock')

async def init(bot):
    @bot.on(events.NewMessage(pattern='🔄 Restart Bot', func=lambda e: e.is_private, from_users=settings.OWNERS))
    async def handler(event):
        await event.delete()
        m = await event.respond('<b>Checking for plugin updates…</b>')
        
        try:
            with open(MAGIC_FILE, 'w') as fd:
                fd.write('{}\n{}\n'.format(m.chat_id, m.id))

            await m.edit('Plugins updated. Restarting…')
        except OSError:
            await m.edit('Plugins updated. Will not notify after restart. Restarting…')

        try:
            python = sys.executable
            os.execl(python, python, *sys.argv)

        except Exception:
            await m.edit('Error on disconnect, this is a bug')

    try:
        with open(MAGIC_FILE) as fd:
            chat_id, msg_id = map(int, fd)
            await bot.edit_message(chat_id, msg_id, 'Plugins updated.')

        os.unlink(MAGIC_FILE)
    except OSError:
        pass