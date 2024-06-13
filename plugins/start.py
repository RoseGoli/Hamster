from telethon import events

async def init(bot):
    @bot.on(events.NewMessage(pattern='^[\/\#\!\.]start$', from_users=1692387237))
    async def handler(event):
        user = await event.get_sender()
        await event.reply(f'Hey <b>{user.first_name}</b>!')