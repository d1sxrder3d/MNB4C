# bots/admin_bot/bot.py
import asyncio
import logging
import os
from typing import List

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import ReplyKeyboardBuilder,  InlineKeyboardBuilder
from aiogram.types.keyboard_button import KeyboardButton
from aiogram.types.inline_keyboard_button import InlineKeyboardButton

from dotenv import load_dotenv

from db.giveaways_db.giveaways_db import GiveawayDB
from db.admins_db.admins_db import AdminDB
from core.admin.admin import Admin, Subscription
from core.date.date import Date
from core.giveaway.giveaway import Giveaways

load_dotenv()

BOT_TOKEN = os.getenv("ADMIN_BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

if BOT_TOKEN is None:
    logging.error("Переменная окружения USERS_BOT_TOKEN не установлена!")
    exit(1)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

giveaway_db = GiveawayDB()
admin_db = AdminDB()

giveaway_db.create_table() 
admin_db.create_table() 

class AdminStates(StatesGroup):
    wait_for_subscription = State()

async def load_data():

    admins = {}

    admins_data = admin_db.get_all_admins()

    for admin_data in admins_data:
        admin_id, admin_name, subscription, giveaways = admin_data
        admin = Admin(admin_id, admin_name, subscription, giveaways)
        admins[admin_id] = admin
        
    return admins

async def register_admin(message):

    admin_id = message.from_user.id 
    admin_name = message.from_user.full_name if message.from_user.full_name is not None else "None"
    
    if admin_name is not None: 
        admins[admin_id] = Admin(admin_id, admin_name)
        admin_db.add_admin(admin_id, admin_name)
    else: 
        admins[admin_id] = Admin(admin_id, "None")
        admin_db.add_admin(admin_id, "None")
        
    
@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):

    if message.from_user.id not in admins.keys(): # type: ignore
        await register_admin(message)
        await state.set_state(AdminStates.wait_for_subscription)
    else:
        pass # Когда админ уже регнут, проверяем его subscription и какйфуем 
    

@dp.message(AdminStates.wait_for_subscription)
async def wait_for_subscription(message: types.Message, state: FSMContext):
    builder = InlineKeyboardBuilder()
    
    Subscribe = InlineKeyboardButton(text="Подписаться", callback_data="subscribe")
    AboutSubscribtions = InlineKeyboardButton(text="О подписках", callback_data="about_subscribtions")

    builder.add(Subscribe)
    builder.add(AboutSubscribtions)

    await message.answer("Хей, кажется тебе стоит подписаться с начала!", reply_markup=builder.as_markup())




async def start_admin_bot():

    global admins

    admins = await load_data()

    try:

        await dp.start_polling(bot)

    finally:

        await bot.session.close()

   
    
