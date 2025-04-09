# bots/admin_bot/bot.py
import asyncio
import logging
import os
from typing import List

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from dotenv import load_dotenv

from db.giveaway_db.giveaway_db import GiveawayDB
from core.giveaway.giveaway import Giveaways

load_dotenv()

BOT_TOKEN = os.getenv("ADMIN_BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Initialize the database
giveaway_db = GiveawayDB()
giveaway_db.create_contests_table() # Create table when bot starts

class ContestRegistration(StatesGroup):
    """States for registering a new contest."""
    waiting_for_contest_name = State()
    waiting_for_contest_channels = State()
    waiting_for_contest_end_date = State()
    waiting_for_contest_is_in_catalog = State()

@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    """Handles the /start command for the admin bot."""
    await message.answer("Добро пожаловать в панель управления конкурсами! Для начала регистрации нового конкурса, введите его название:")
    await state.set_state(ContestRegistration.waiting_for_contest_name)

@dp.message(ContestRegistration.waiting_for_contest_name)
async def get_contest_name(message: types.Message, state: FSMContext):
    """Gets the contest name."""
    await state.update_data(contest_name=message.text)
    await message.answer("Отлично! Теперь введите названия телеграм каналов, на которые нужно подписаться, через запятую (например: @channel1, @channel2, @channel3):")
    await state.set_state(ContestRegistration.waiting_for_contest_channels)

@dp.message(ContestRegistration.waiting_for_contest_channels)
async def get_contest_channels(message: types.Message, state: FSMContext):
    """Gets the contest channels."""
    await state.update_data(contest_channels=message.text)
    await message.answer("Хорошо! Теперь введите дату окончания конкурса (в формате ГГГГ-ММ-ДД):")
    await state.set_state(ContestRegistration.waiting_for_contest_end_date)

@dp.message(ContestRegistration.waiting_for_contest_end_date)
async def get_contest_end_date(message: types.Message, state: FSMContext):
    """Gets the contest end date."""
    await state.update_data(contest_end_date=message.text)
    await message.answer("Добавить конкурс в каталог? (y/n):")
    await state.set_state(ContestRegistration.waiting_for_contest_is_in_catalog)

@dp.message(ContestRegistration.waiting_for_contest_is_in_catalog)
async def get_contest_is_in_catalog(message: types.Message, state: FSMContext):
    """Gets the contest is_in_catalog and completes the registration."""
    is_in_catalog = message.text.lower() == "y"
    await state.update_data(contest_is_in_catalog=is_in_catalog)

    data = await state.get_data()
    contest_name = data.get("contest_name")
    contest_channels_str = data.get("contest_channels")
    contest_end_date = data.get("contest_end_date")
    contest_is_in_catalog = data.get("contest_is_in_catalog")
    contest_channels = [channel.strip() for channel in contest_channels_str.split(",")] if contest_channels_str else []
    creator_id = message.from_user.id

    # Save the contest to the database
    giveaway_db.add_contest(
        giveaway_title=contest_name,
        creator_id=creator_id,
        needed_channels=contest_channels,
        is_in_catalog=contest_is_in_catalog,
        end_date=contest_end_date
    )

    await message.answer(f"Конкурс '{contest_name}' успешно зарегистрирован!\n"
                         f"Каналы для подписки: {', '.join(contest_channels)}\n"
                         f"Дата окончания: {contest_end_date}\n"
                         f"Добавлен в каталог: {'Да' if contest_is_in_catalog else 'Нет'}")
    await state.clear()

@dp.message(Command("list"))
async def list_contests(message: types.Message):
    """Lists all registered contests."""
    contests = giveaway_db.get_all_contests()
    if contests:
        response = "Список зарегистрированных конкурсов:\n"
        for contest in contests:
            channels = giveaway_db.get_channels_for_contest(contest[0])
            response += f"ID: {contest[0]}, Название: {contest[1]}, Создатель: {contest[2]}, В каталоге: {'Да' if contest[3] else 'Нет'}, Каналы: {', '.join(channels) if channels else 'Не указаны'}, Дата окончания: {contest[5]}\n"
    else:
        response = "Пока нет зарегистрированных конкурсов."
    await message.answer(response)

@dp.message()
async def echo(message: types.Message):
    await message.answer(message.text)

async def start_admin_bot():
    """Starts the admin bot."""
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

