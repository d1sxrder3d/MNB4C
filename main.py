import asyncio
from bots.users_bot.bot import start_users_bot
from bots.admin_bot.bot import start_admin_bot

async def start_bot():
    await asyncio.gather(start_users_bot(), start_admin_bot())



if __name__ == "__main__":
    # if input() == "start":
    asyncio.run(start_bot())