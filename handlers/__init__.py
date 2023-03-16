import os
import telebot
import telebot.types as tt


bot_service = telebot.TeleBot(os.environ['BOT_TOKEN'])


@bot_service.message_handler(commands=['start', 'help'])
def send_welcome(message):
    print(message)
    bot_service.send_message(message.chat.id, "Это бот, который поможет найти нужный фильм или сериал :)")


@bot_service.message_handler(commands=['button'])
def button_message(message):
    markup = tt.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = tt.KeyboardButton("Кнопка Раз")
    item2 = tt.KeyboardButton("Кнопка Два")
    markup.add(item1, item2)
    bot_service.send_message(message.chat.id, 'Выберите из меню', reply_markup=markup)


@bot_service.message_handler(func=lambda m: True)
def echo_all(message):
    bot_service.reply_to(message, message.text)
