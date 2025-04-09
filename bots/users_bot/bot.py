import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from dotenv import load_dotenv


load_dotenv()


BOT_TOKEN = os.getenv("BOT_TOKEN")


logging.basicConfig(level=logging.INFO)


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()



@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я твой бот.")



@dp.message()
async def echo(message: types.Message):
    await message.answer(message.text)



async def main():
    
    try:
        await dp.start_polling(bot)

    finally:
        
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
