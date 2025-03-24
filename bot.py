import telebot
import pickle

TOKEN = '7978854259:AAFx7lEricXAZBMFWVE0D8W3WgbWph5CIaY'
bot = telebot.TeleBot(TOKEN)

# Зберігання даних користувачів
users_data = {}

def save_data():
    with open("users.pkl", "wb") as f:
        pickle.dump(users_data, f)

def load_data():
    global users_data
    try:
        with open("users.pkl", "rb") as f:
            users_data = pickle.load(f)
    except FileNotFoundError:
        users_data = {}

load_data()

# Доступні години для запису в душ
time_slots = {
    1: "6:00 - 7:00",
    2: "9:00 - 10:00",
    3: "12:00 - 13:00",
    4: "15:00 - 16:00",
    5: "18:00 - 19:00",
    6: "21:00 - 22:00"
}

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    if user_id in users_data:
        main_menu(message)
    else:
        bot.send_message(user_id, "Реєстрація\nВведіть ваше ПІБ:")
        bot.register_next_step_handler(message, register_name)

def register_name(message):
    user_id = message.chat.id
    users_data[user_id] = {"name": message.text}
    bot.send_message(user_id, "Вкажіть вашу стать (ч/ж):")
    bot.register_next_step_handler(message, register_gender)

def register_gender(message):
    user_id = message.chat.id
    users_data[user_id]["gender"] = message.text
    bot.send_message(user_id, "Вкажіть ваш гуртожиток:")
    bot.register_next_step_handler(message, register_dorm)

def register_dorm(message):
    user_id = message.chat.id
    users_data[user_id]["dorm"] = message.text
    users_data[user_id]["shower_time"] = None
    save_data()
    main_menu(message)

def main_menu(message):
    user_id = message.chat.id
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("1. Інформація про акаунт", "2. Запис у душ")
    bot.send_message(user_id, "Меню:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "1. Інформація про акаунт")
def account_info(message):
    user_id = message.chat.id
    user = users_data.get(user_id, {})
    text = (f"Інформація про акаунт:\nПІБ: {user.get('name', 'Невідомо')}\n"
            f"Стать: {user.get('gender', 'Невідомо')}\n"
            f"Гуртожиток: {user.get('dorm', 'Невідомо')}\n")
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Перереєструватись", "Назад")
    bot.send_message(user_id, text, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Перереєструватись")
def re_register(message):
    user_id = message.chat.id
    if user_id in users_data:
        del users_data[user_id]
        save_data()
    start(message)

@bot.message_handler(func=lambda message: message.text == "Назад")
def back_to_menu(message):
    main_menu(message)

@bot.message_handler(func=lambda message: message.text == "2. Запис у душ")
def shower_booking(message):
    user_id = message.chat.id
    text = "Доступні години:\n" + "\n".join([f"{k}. {v}" for k, v in time_slots.items()])
    bot.send_message(user_id, text)
    bot.send_message(user_id, "Оберіть номер бажаного часу:")
    bot.register_next_step_handler(message, set_shower_time)

def set_shower_time(message):
    user_id = message.chat.id
    try:
        choice = int(message.text)
        if choice in time_slots:
            users_data[user_id]["shower_time"] = time_slots[choice]
            save_data()
            bot.send_message(user_id, f"Ви записані на {time_slots[choice]}\nВаш порядковий номер: {list(time_slots.keys()).index(choice) + 1}")
            main_menu(message)
        else:
            bot.send_message(user_id, "Некоректний вибір. Виберіть правильний номер.")
            shower_booking(message)
    except ValueError:
        bot.send_message(user_id, "Будь ласка, введіть число.")
        shower_booking(message)

bot.polling(none_stop=True)