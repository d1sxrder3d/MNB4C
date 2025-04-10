# bots/admin_bot/bot.py
import asyncio
import logging
import os
from typing import List

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton
from dotenv import load_dotenv

from db.giveaway_db.giveaway_db import GiveawayDB
from core.admins.admin import Admin, Subscription
from core.date.date import Date
from core.giveaway.giveaway import Giveaways

load_dotenv()

BOT_TOKEN = os.getenv("ADMIN_BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Initialize the database
giveaway_db = GiveawayDB()

giveaway_db.create_contests_table()  # Create table when bot starts

# Dictionary to store admin users (replace with a database in a real application)
admin_users: dict[int, Admin] = {}


class ContestRegistration(StatesGroup):
    #States for registering a new contest.
    waiting_for_contest_name = State()
    waiting_for_contest_channels = State()
    waiting_for_contest_end_date = State()
    waiting_for_contest_is_in_catalog = State()


# Function to create the main menu keyboard
def get_main_menu_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text="Создать розыгрыш"),
        KeyboardButton(text="Мои розыгрыши")
    )
    builder.row(
        KeyboardButton(text="Информация о боте"),
        KeyboardButton(text="Список конкурсов")
    )
    return builder.as_markup(resize_keyboard=True)


@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    """Handles the /start command for the admin bot."""
    user_id = message.from_user.id
    user_name = message.from_user.full_name

    # Check if the user is already registered as an admin
    if user_id not in admin_users:
        admin_users[user_id] = Admin(user_id=user_id, user_name=user_name)

    await message.answer(
        "Добро пожаловать в панель управления конкурсами!\nВыберите действие:",
        reply_markup=get_main_menu_keyboard()
    )
    await state.clear()  # clear state when start command


@dp.message(lambda message: message.text == "Создать розыгрыш")
async def process_create_giveaway(message: types.Message, state: FSMContext):
    """Handles the 'create_giveaway' button."""
    await message.answer("Введите название розыгрыша:", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(ContestRegistration.waiting_for_contest_name)


@dp.message(lambda message: message.text == "Мои розыгрыши")
async def process_my_giveaways(message: types.Message):
    """Handles the 'my_giveaways' button."""
    user_id = message.from_user.id
    admin = admin_users.get(user_id)
    admin.giveaways = giveaway_db.get_contest_by_id(admin.user_id)
    if admin:
        if admin.giveaways:
            response = "Ваши розыгрыши:\n"
            for giveaway in admin.giveaways:
                response += f"- {giveaway.title} (ID: {giveaway.id})\n"
        # elif giveaway_db.get_contest_by_id(admin.user_id):
        #     response = "Ваши розыгрыши:\n"
        #     for giveaway in admin.giveaways:
        #         response += f"- {giveaway.title} (ID: {giveaway.id})\n"

        else:
            response = "У вас пока нет созданных розыгрышей."
    else:
        response = "Вы не зарегистрированы как администратор."
    await message.answer(response, reply_markup=get_main_menu_keyboard())


@dp.message(lambda message: message.text == "Информация о боте")
async def process_bot_info(message: types.Message):
    """Handles the 'bot_info' button."""
    await message.answer("Это бот для управления розыгрышами. \nСоздан для удобного создания и отслеживания розыгрышей.", reply_markup=get_main_menu_keyboard())


@dp.message(lambda message: message.text == "Список конкурсов")
async def process_list_contests(message: types.Message):
    """Handles the 'list_contests' button."""
    await list_contests(message)


@dp.message(ContestRegistration.waiting_for_contest_name)
async def get_contest_name(message: types.Message, state: FSMContext):
    
    await state.update_data(contest_name=message.text)
    await message.answer(
        "Отлично! Теперь введите названия телеграм каналов, на которые нужно подписаться, через запятую (например: @channel1, @channel2, @channel3):",
        reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(ContestRegistration.waiting_for_contest_channels)


@dp.message(ContestRegistration.waiting_for_contest_channels)
async def get_contest_channels(message: types.Message, state: FSMContext):
    """Gets the contest channels."""
    await state.update_data(contest_channels=message.text)
    await message.answer("Хорошо! Теперь введите дату окончания конкурса (в формате ДД-ММ):", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(ContestRegistration.waiting_for_contest_end_date)


@dp.message(ContestRegistration.waiting_for_contest_end_date)
async def get_contest_end_date(message: types.Message, state: FSMContext):
    """Gets the contest end date."""
    await state.update_data(contest_end_date=message.text)

    # Create reply keyboard for is_in_catalog
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="Да"))
    builder.add(KeyboardButton(text="Нет"))
    builder.adjust(2)

    await message.answer("Добавить конкурс в каталог?", reply_markup=builder.as_markup(resize_keyboard=True, one_time_keyboard=True))
    await state.set_state(ContestRegistration.waiting_for_contest_is_in_catalog)


@dp.message(ContestRegistration.waiting_for_contest_is_in_catalog)
async def get_contest_is_in_catalog(message: types.Message, state: FSMContext):
    """Gets the contest is_in_catalog and completes the registration."""
    is_in_catalog = message.text == "Да"
    await state.update_data(contest_is_in_catalog=is_in_catalog)

    data = await state.get_data()
    contest_name = data.get("contest_name")
    contest_channels_str = data.get("contest_channels")
    contest_end_date_str = data.get("contest_end_date")
    contest_is_in_catalog = data.get("contest_is_in_catalog")
    contest_channels = [channel.strip() for channel in contest_channels_str.split(",")] if contest_channels_str else []
    creator_id = message.from_user.id

    # Parse the end date
    if '-' in contest_end_date_str:
        day, month = map(int, contest_end_date_str.split('-'))
    elif '.' in contest_end_date_str:
        day, month = map(int, contest_end_date_str.split('.'))
    else: 
        await message.answer("Неправильный формат даты")
        await state.set_state(ContestRegistration.waiting_for_contest_is_in_catalog)
        return

    contest_end_date = Date(day=day, month=month)

    # Save the contest to the database
    giveaway_db.add_contest(
        giveaway_title=contest_name,
        creator_id=creator_id,
        needed_channels=contest_channels,
        is_in_catalog=contest_is_in_catalog,
        end_date=contest_end_date.__str__()
    )
    # Get the giveaway id
    giveaway_id = giveaway_db.get_all_contests()[-1][0]

    # Create a Giveaway object
    giveaway = Giveaways(
        giveaway_id=giveaway_id,
        title=contest_name,
        creator_id=creator_id,
        end_date=contest_end_date,
        needed_chanels=contest_channels,
        is_in_catalog=is_in_catalog
    )

    # Add the giveaway to the admin's list
    admin = admin_users.get(creator_id)
    if admin:
        admin.add_giveaway(giveaway)

    await message.answer(
        f"Розыгрыш '{contest_name}' успешно зарегистрирован!\n"
        f"Каналы для подписки: {', '.join(contest_channels)}\n"
        f"Дата окончания: {contest_end_date}\n"
        f"Добавлен в каталог: {'Да' if contest_is_in_catalog else 'Нет'}",
        reply_markup=get_main_menu_keyboard()
    )
    await state.clear()


@dp.message(Command("list"))
async def list_contests(message: types.Message):

    """Lists all registered contests."""
    contests = giveaway_db.get_all_contests()
    if contests:
        response = "Список зарегистрированных конкурсов:\n"
        for contest in contests:
            channels = giveaway_db.get_channels_for_contest(contest[0])
            response += f"Название: {contest[1]}, Каналы: {', '.join(channels) if channels else 'Не указаны'}, Дата окончания: {contest[5]}\n"
    else:
        response = "Пока нет зарегистрированных конкурсов."
    await message.answer(response, reply_markup=get_main_menu_keyboard())


@dp.message()
async def echo(message: types.Message):
    await message.answer(message.text)


async def start_admin_bot():
    """Starts the admin bot."""
    try:
        await dp.start_polling(bot)
        
    finally:
        await bot.session.close()
