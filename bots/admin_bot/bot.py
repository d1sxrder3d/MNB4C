# bots/admin_bot/bot.py
import asyncio
import logging
import os
from typing import List

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton, InlineKeyboardBuilder, InlineKeyboardButton
from dotenv import load_dotenv

from db.giveaways_db.giveaways_db import GiveawayDB
from db.admins_db.admins_db import AdminDB
from core.admin.admin import Admin, Subscription
from core.date.date import Date
from core.giveaway.giveaway import Giveaways

load_dotenv()

BOT_TOKEN = os.getenv("ADMIN_BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

giveaway_db = GiveawayDB()
admin_db = AdminDB()

giveaway_db.create_table() 
admin_db.create_table() 



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
    admin_name = message.from_user.full_name

    if admin_name != None: 
        pass #кога есть ник
    else: 
        pass #когда ника нет 
    
    
    
    

@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    global admins

    await admins = load_data()

    if message.from_user.id not in admins:
        await register_admin(message)

    await state.clear()


async def start_admin_bot():

    

    try:

        await dp.start_polling(bot)

    finally:

        await bot.session.close()

   
    
