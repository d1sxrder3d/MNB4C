# bots/admin_bot/bot.py
import asyncio
import logging
import os
from typing import List, Optional

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import ReplyKeyboardBuilder,  InlineKeyboardBuilder
from aiogram.types.keyboard_button import KeyboardButton
from aiogram.types.inline_keyboard_button import InlineKeyboardButton

from dotenv import load_dotenv

from db.core_db.giveaways_db.giveaways_db import GiveawayDB
from db.core_db.admins_db.admins_db import AdminDB
from db.core_db.subscriptions_db.subscriptions_db import SubscriptionDB
from core.admin.admin import Admin, Subscription
from core.date.date import Date
from core.giveaway.giveaway import Giveaways

import bots.admin_bot.text as text
import bots.admin_bot.bot_messages as send_messages






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
subscription_db = SubscriptionDB()



giveaway_db.create_table() 
admin_db.create_table()
subscription_db.create_table()


class AdminStates(StatesGroup):
    wait_for_subscription = State()

async def load_data() -> dict:

    admins = {}

    admins_data = admin_db.get_all_admins()

    for admin_data in admins_data:
        admin_id, admin_name, subscription_id = admin_data 
        subscription = subscription_db.get_subscription_by_id(subscription_id)

        admin = Admin(admin_id, admin_name, subscription) 
        admins[admin_id] = admin
        
    return admins


async def delete_last_messages():
    

async def register_admin(message: types.Message): # Сделали асинхронной

    admin_id = message.from_user.id #type: ignore
    admin_name = message.from_user.full_name if message.from_user.full_name is not None else "None" #type: ignore
    
    if admin_name is not None: 
        admins[admin_id] = Admin(admin_id, admin_name)
        admin_db.add_admin(admin_id, admin_name)
    else: 
        admins[admin_id] = Admin(admin_id, "None")
        admin_db.add_admin(admin_id, "None")
    
    await message.answer("Хей, кажется тебе стоит подписаться с начала!") # Добавили сообщение
    
@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):

    if message.from_user.id not in admins: #type: ignore
        await register_admin(message) # Добавили await
        await state.set_state(AdminStates.wait_for_subscription)
    elif admins[message.from_user.id].subscription.subscriptin_level == Subscription.SubscriptionLevel.NONE: # type: ignore
        await wait_for_subscription(message, state)
    else:
        await message.answer("Ты уже зарегистрирован и у тебя есть подписка!") # Добавили сообщение
    

@dp.message(AdminStates.wait_for_subscription)
async def wait_for_subscription(message: types.Message, state: FSMContext):
    await send_messages.wait_for_subscription(message, state)
    





@dp.callback_query(lambda c: c.data == "subscribe")
async def process_subscribe_callback(callback_query: types.CallbackQuery):
    await send_messages.subscribe(bot, callback_query)
    
    # Здесь можно добавить логику для обработки подписки


@dp.callback_query(lambda c: c.data == "about_subscribtions")
async def process_about_subscribtions_callback(callback_query: types.CallbackQuery):
    await send_messages.about_subscribtions(bot, callback_query)
   
@dp.callback_query(lambda c: c.data == "about_basic")    
async def process_about_basic(callback_query: types.CallbackQuery):
    
    await bot.send_message(callback_query.from_user.id, text.aboutBasic)

@dp.callback_query(lambda c: c.data == "about_premium")    
async def process_about_premium(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, text.aboutPremium)
    







@dp.callback_query(lambda c: c.data == "back_to_subscribe")
async def process_back_to_subscribe_callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    await wait_for_subscription(callback_query.message, AdminStates.wait_for_subscription)



@dp.callback_query(lambda c: c.data == "basic")
async def process_basic_callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    
    await bot.send_message(callback_query.from_user.id, "Вы выбрали подписку \"Базовая\"")

    await bot.send_message(callback_query.from_user.id, "типо оплата")
    
@dp.callback_query(lambda c: c.data == "premium")
async def process_premium_callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    
    await bot.send_message(callback_query.from_user.id, "Вы выбрали подписку \"Продвинутая\"")

    await bot.send_message(callback_query.from_user.id, "типо оплата")

    admins[callback_query.from_user.id]





async def start_admin_bot():

    global admins

    admins = await load_data()

    try:

        await dp.start_polling(bot)

    finally:

        await bot.session.close()
