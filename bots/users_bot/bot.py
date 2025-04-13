# bots/admin_bot/bot.py
import asyncio
import logging
import os
from typing import List

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types.keyboard_button import KeyboardButton
from dotenv import load_dotenv



load_dotenv()

BOT_TOKEN = os.getenv("USERS_BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

if BOT_TOKEN is None:
    logging.error("Переменная окружения USERS_BOT_TOKEN не установлена!")
    exit(1)
    
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

async def start_users_bot():
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
