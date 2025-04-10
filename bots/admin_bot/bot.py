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

from db.giveaway_db.giveaway_db import GiveawayDB
from db.admins_db.admins_db import AdminDB
from core.admins.admin import Admin, Subscription
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


admin_users: dict[int, Admin] = {}


giveaways: dict[int, Giveaways] = {}


messages_to_delete: List[int] = []


class ContestRegistration(StatesGroup):

    waiting_for_contest_name = State()
    waiting_for_contest_channels = State()
    waiting_for_contest_end_date = State()
    waiting_for_contest_is_in_catalog = State()


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


async def load_data():
    # C db при запуске 
    global admin_users, giveaways

    
    all_admins = admin_db.get_all_admins()

    for admin_data in all_admins:

        admin_id, admin_name, subscription, giveaway_ids = admin_data

        admin_users[admin_id] = Admin(
            user_id=admin_id,
            user_name=admin_name,
            subscription=subscription,
            giveaways=giveaway_ids
        )

    
    all_giveaways = giveaway_db.get_all_contests()

    for giveaway_data in all_giveaways:

        giveaway_id, title, is_in_catalog, needed_channels_str, end_date_str, tickets_count, winners_count, winners = giveaway_data
        needed_channels = needed_channels_str.split(',') if needed_channels_str else []

        if end_date_str:
            day, month = map(int, end_date_str.split('.'))
            end_date = Date(day=day, month=month)
        else:
            end_date = None

        giveaways[giveaway_id] = Giveaways(
            giveaway_id=giveaway_id,
            title=title,
            end_date=end_date,
            needed_chanels=needed_channels,
            is_in_catalog=is_in_catalog
        )


async def delete_last_messages(chat_id: int, message_ids: List[int]):
    # Хуйня какая то сделать удаления
    for message_id in message_ids:
        try:
            await bot.delete_message(chat_id, message_id)
        except Exception as e:
            logging.error(f"Error deleting message {message_id}: {e}")


@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user_name = message.from_user.full_name

    if user_id not in admin_users:

        admin_users[user_id] = Admin(user_id=user_id, user_name=user_name, subscription=Subscription(), giveaways=[])  # Исправлено
        admin_db.add_admin(user_id, user_name, Subscription(), [])  

    msg = await message.answer(
        "Добро пожаловать в панель управления конкурсами!\nВыберите действие:",
        reply_markup=get_main_menu_keyboard()
    )

    messages_to_delete.extend([message.message_id, msg.message_id])

    await state.clear()


@dp.message(lambda message: message.text == "Создать розыгрыш")
async def process_create_giveaway(message: types.Message, state: FSMContext):

    msg = await message.answer("Введите название розыгрыша:", reply_markup=types.ReplyKeyboardRemove())
    
    messages_to_delete.extend([message.message_id, msg.message_id])

    await state.set_state(ContestRegistration.waiting_for_contest_name)


@dp.message(lambda message: message.text == "Мои розыгрыши")
async def process_my_giveaways(message: types.Message):

    user_id = message.from_user.id

    admin = admin_users.get(user_id)

    builder = InlineKeyboardBuilder()

    if admin:
        response = "Ваши розыгрыши:\n"

        if admin.giveaways:
            for giveaway_id in admin.giveaways:

                giveaway = giveaways.get(giveaway_id)

                if giveaway:

                    builder.add(InlineKeyboardButton(text=giveaway.title, callback_data=f"giveaway_{giveaway_id}"))
            
            builder.adjust(1)

            msg = await message.answer(response, reply_markup=builder.as_markup(), one_time_keyboard=True)
            
            messages_to_delete.extend([message.message_id, msg.message_id])

        else:

            response = "У вас пока нет созданных розыгрышей."
            
            msg = await message.answer(response, reply_markup=get_main_menu_keyboard())
            
            messages_to_delete.extend([message.message_id, msg.message_id])
    else:
        response = "Вы не зарегистрированы как администратор."
        
        msg = await message.answer(response, reply_markup=get_main_menu_keyboard())
        
        messages_to_delete.extend([message.message_id, msg.message_id])


@dp.callback_query(lambda c: c.data.startswith("giveaway_"))
async def process_giveaway_callback(callback_query: types.CallbackQuery):

    giveaway_id = int(callback_query.data.split("_")[1])

    giveaway = giveaways.get(giveaway_id)

    if giveaway:
        
        msg = await callback_query.message.answer(
            f"Название: {giveaway.title}\n"
            f"Каналы для подписки: {', '.join(giveaway.needed_channels)}\n"
            f"Дата окончания: {giveaway.end_date}")
        
        messages_to_delete.extend([callback_query.message.message_id, msg.message_id])


@dp.message(lambda message: message.text == "Информация о боте")
async def process_bot_info(message: types.Message):

    msg = await message.answer(
        "Это бот для управления розыгрышами. \nСоздан для удобного создания и отслеживания розыгрышей.",
        reply_markup=get_main_menu_keyboard()
    )
    
    messages_to_delete.extend([message.message_id, msg.message_id])


@dp.message(lambda message: message.text == "Список конкурсов")
async def process_list_contests(message: types.Message):
    await list_contests(message)


@dp.message(ContestRegistration.waiting_for_contest_name)
async def get_contest_name(message: types.Message, state: FSMContext):
    await state.update_data(contest_name=message.text)
    
    msg = await message.answer(
        "Отлично! Теперь введите названия телеграм каналов, на которые нужно подписаться, через запятую (например: @channel1, @channel2, @channel3):",
        reply_markup=types.ReplyKeyboardRemove()
    )
    
    messages_to_delete.extend([message.message_id, msg.message_id])
    
    await state.set_state(ContestRegistration.waiting_for_contest_channels)


@dp.message(ContestRegistration.waiting_for_contest_channels)
async def get_contest_channels(message: types.Message, state: FSMContext):
    
    await state.update_data(contest_channels=message.text)
    
    msg = await message.answer("Хорошо! Теперь введите дату окончания конкурса (в формате ДД.ММ):",
                         reply_markup=types.ReplyKeyboardRemove())
    
    messages_to_delete.extend([message.message_id, msg.message_id])
    
    await state.set_state(ContestRegistration.waiting_for_contest_end_date)


@dp.message(ContestRegistration.waiting_for_contest_end_date)
async def get_contest_end_date(message: types.Message, state: FSMContext):

    await state.update_data(contest_end_date=message.text)

    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="Да"))
    builder.add(KeyboardButton(text="Нет"))
    builder.adjust(2)

    msg = await message.answer("Добавить конкурс в каталог?",
                         reply_markup=builder.as_markup(resize_keyboard=True, one_time_keyboard=True))
    
    messages_to_delete.extend([message.message_id, msg.message_id])
    
    await state.set_state(ContestRegistration.waiting_for_contest_is_in_catalog)


@dp.message(ContestRegistration.waiting_for_contest_is_in_catalog)
async def get_contest_is_in_catalog(message: types.Message, state: FSMContext):
    is_in_catalog = message.text == "Да"
    await state.update_data(contest_is_in_catalog=is_in_catalog)

    data = await state.get_data()
    contest_name = data.get("contest_name")
    contest_channels_str = data.get("contest_channels")
    contest_end_date_str = data.get("contest_end_date")
    contest_is_in_catalog = data.get("contest_is_in_catalog")
    contest_channels = [channel.strip() for channel in contest_channels_str.split(",")] if contest_channels_str else []
    creator_id = message.from_user.id

    if '.' in contest_end_date_str:
        day, month = map(int, contest_end_date_str.split('.'))
    else:
        msg = await message.answer("Неправильный формат даты, введите в формате ДД.ММ")
        messages_to_delete.extend([message.message_id, msg.message_id])
        await state.set_state(ContestRegistration.waiting_for_contest_end_date)
        return

    contest_end_date = Date(day=day, month=month)

    giveaway_db.add_contest(
        giveaway_title=contest_name,
        needed_channels=contest_channels,
        is_in_catalog=contest_is_in_catalog,
        end_date=contest_end_date.__str__()
    )

    giveaway_id = giveaway_db.get_all_contests()[-1][0]

    giveaway = Giveaways(
        giveaway_id=giveaway_id,
        title=contest_name,
        end_date=contest_end_date,
        needed_chanels=contest_channels,
        is_in_catalog=is_in_catalog
    )

    giveaways[giveaway_id] = giveaway

    admin = admin_users.get(creator_id)
    if admin:
        admin.add_giveaway(giveaway_id)
        admin_db.update_admin(admin.user_id, admin.user_name, admin.subscription, admin.giveaways)

    msg = await message.answer(
        f"Розыгрыш '{contest_name}' успешно зарегистрирован!\n"
        f"Каналы для подписки: {', '.join(contest_channels)}\n"
        f"Дата окончания: {contest_end_date}\n"
        f"Добавлен в каталог: {'Да' if contest_is_in_catalog else 'Нет'}",
        reply_markup=get_main_menu_keyboard()
    )
    messages_to_delete.extend([message.message_id, msg.message_id])
    await state.clear()


@dp.message(Command("list"))
async def list_contests(message: types.Message):
    contests = giveaway_db.get_all_contests()
    if contests:
        response = "Список зарегистрированных конкурсов:\n"

        for contest in contests:
            channels = giveaway_db.get_channels_for_contest(contest[0])
            response += f"Название: {contest[1]}, Каналы: {', '.join(channels) if channels else 'Не указаны'}, Дата окончания: {contest[4]}\n"
    else:
        response = "Пока нет зарегистрированных конкурсов."

    msg = await message.answer(response, reply_markup=get_main_menu_keyboard())
    messages_to_delete.extend([message.message_id, msg.message_id])


@dp.message()
async def echo(message: types.Message):
    msg = await message.answer(message.text)
    messages_to_delete.extend([message.message_id, msg.message_id])


async def start_admin_bot():

    await load_data()

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
    
    # await delete_last_messages(message.chat.id, messages_to_delete)
    messages_to_delete.clear()
