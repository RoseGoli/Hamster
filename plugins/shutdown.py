from telethon import events

async def init(bot):
    @bot.on(events.NewMessage(pattern='^[\/\#\!\.]shut$', from_users=1692387237))
    async def handler(event):
        await event.respond('<b>Shutted Down !</b>')
        bot.disconnect()