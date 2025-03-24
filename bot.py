import telebot

bot = telebot.TeleBot('7978854259:AAFx7lEricXAZBMFWVE0D8W3WgbWph5CIaY')

@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id, 'Привіт, пострижись, ти ЛОХ блять помийся!')

bot.polling(non_stop=True)