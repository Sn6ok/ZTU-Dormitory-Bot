from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor

TOKEN = "7978854259:AAFx7lEricXAZBMFWVE0D8W3WgbWph5CIaY"
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

queue = {"10:00": [], "13:00": []}  # Черга за часами

# Головне меню
kb_main = ReplyKeyboardMarkup(resize_keyboard=True)
kb_main.add(KeyboardButton("Записатися"), KeyboardButton("Список"))

# Меню вибору часу
kb_time = ReplyKeyboardMarkup(resize_keyboard=True)
kb_time.add(KeyboardButton("10:00"), KeyboardButton("13:00"), KeyboardButton("Назад"))

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Привіт! Обери дію:", reply_markup=kb_main)

@dp.message_handler(lambda message: message.text == "Записатися")
async def choose_time(message: types.Message):
    await message.answer("Оберіть час для запису:", reply_markup=kb_time)

@dp.message_handler(lambda message: message.text in ["10:00", "13:00"])
async def join_queue(message: types.Message):
    time_slot = message.text
    user_name = message.from_user.full_name
    
    if user_name not in queue[time_slot]:
        queue[time_slot].append(user_name)
        await message.answer(f"{user_name}, ви записані на {time_slot}! Ваш номер: {len(queue[time_slot])}.", reply_markup=kb_main)
    else:
        await message.answer("Ви вже записані на цей час!", reply_markup=kb_main)

@dp.message_handler(lambda message: message.text == "Список")
async def show_queue(message: types.Message):
    queue_list = "\n".join([f"⏰ {time}:\n" + "\n".join([f"{i+1}. {name}" for i, name in enumerate(queue[time])]) if queue[time] else f"⏰ {time}: (порожньо)" for time in queue])
    await message.answer(f"📋 Черга на душ:\n\n{queue_list}")

@dp.message_handler(lambda message: message.text == "Назад")
async def back(message: types.Message):
    await message.answer("Обери дію:", reply_markup=kb_main)

@dp.message_handler(commands=['clear'])
async def clear_queue(message: types.Message):
    for time in queue:
        queue[time] = []
    await message.answer("Чергу очищено!")

if name == 'main':
    executor.start_polling(dp, skip_updates=True)