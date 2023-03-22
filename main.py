import os
import telebot
import telebot.types as tt
from dotenv import load_dotenv

from utils import FilmFetch

load_dotenv()  # .env variables

bot_service = telebot.TeleBot(os.environ['BOT_TOKEN'])  # bot instance


@bot_service.message_handler(commands=['start', 'help'])
def send_welcome(message):
    """Welcome message"""
    bot_service.send_message(message.chat.id, "Это бот, который поможет найти нужный фильм или сериал :)")


@bot_service.message_handler(commands=['test'])
def test_message(message):
    """test buttons"""
    markup = tt.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = tt.KeyboardButton("Кнопка Раз")
    item2 = tt.KeyboardButton("Кнопка Два")
    markup.add(item1, item2)
    bot_service.send_message(message.chat.id, 'Выберите из меню', reply_markup=markup)


@bot_service.message_handler(commands=['find'])
def send_film_test(message):
    """test film"""

    url = 'https://api.kinopoisk.dev/v1/movie'
    headers = {"X-API-KEY": os.environ["API_KEY"]}
    params = {'id': 335}
    Fetch = FilmFetch(url, headers, params)
    try:
        info = Fetch.cached_request()['docs'][0]  # кэшированный запрос
        poster = info['poster']['url']
        caption = f"Фильм: {info['name']}\n" \
                  f"Рейтинг: {info['rating']['kp']}\n" \
                  f"Год: {info['year']}\n\n" \
                  f"{info['description']}"

        markup = tt.InlineKeyboardMarkup()

        if info['externalId']['kpHD'] is not None:
            btn_my_site = tt.InlineKeyboardButton(
                text='Смотреть онлайн',
                url=f"https://hd.kinopoisk.ru/film/{info['externalId']['kpHD']}")
            markup.add(btn_my_site)

        bot_service.send_photo(message.chat.id, photo=poster, caption=caption, reply_markup=markup)
    except Exception:
        print("Request unsuccessful")


@bot_service.message_handler(func=lambda m: True)
def echo_all(message):
    """Reply for any other message"""
    bot_service.reply_to(message, "Не понял :/")


if __name__ == "__main__":
    print("bot running")
    bot_service.infinity_polling()







