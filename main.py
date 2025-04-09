import asyncio
from bot.bot import main

async def start_bot():
    await main()

if __name__ == "__main__":
    if input() == "start":
        asyncio.run(start_bot())