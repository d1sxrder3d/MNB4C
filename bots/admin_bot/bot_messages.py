import asyncio
import logging
import os
from typing import List, Optional

from aiogram import Bot, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import ReplyKeyboardBuilder,  InlineKeyboardBuilder
from aiogram.types.keyboard_button import KeyboardButton
from aiogram.types.inline_keyboard_button import InlineKeyboardButton

import bots.admin_bot.text as text





async def wait_for_subscription(message: types.Message, state: FSMContext):
    builder = InlineKeyboardBuilder()
    
    Subscribe = InlineKeyboardButton(text="Подписаться", callback_data="subscribe")
    AboutSubscribtions = InlineKeyboardButton(text="О подписках", callback_data="about_subscribtions")

    builder.add(Subscribe)
    builder.add(AboutSubscribtions)

    builder.adjust(2)
    

    await message.answer("Хей, кажется тебе стоит подписаться с начала!", reply_markup=builder.as_markup())


async def subscribe(bot: Bot, callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    builder = InlineKeyboardBuilder()
    
    Basic = InlineKeyboardButton(text="Базовая", callback_data="basic")
    Premium = InlineKeyboardButton(text="Продвинутая", callback_data="premium")

    builder.add(Basic)
    builder.add(Premium)

    builder.adjust(2)
    
    await bot.send_message(callback_query.from_user.id, "Выберите подписку:", reply_markup=builder.as_markup())
    

async def about_subscribtions(bot: Bot, callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    
    builder = InlineKeyboardBuilder()
    
    backButton = InlineKeyboardButton(text="Назад", callback_data="back_to_subscribe")

    aboutBasicButton = InlineKeyboardButton(text= "О базовой подписке", callback_data="about_basic")
    aboutPremiumButton = InlineKeyboardButton(text= "О премиум подписке", callback_data="about_premium")

    builder.add(aboutBasicButton, aboutPremiumButton, backButton)

    builder.adjust(1)
    
    await bot.send_message(callback_query.from_user.id, text.typesOfSubcriptions, reply_markup=builder.as_markup())