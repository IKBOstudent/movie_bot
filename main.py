import os
import telebot
import telebot.types as tt
from dotenv import load_dotenv

from utils import FilmFetch
from handlers import form_result


load_dotenv()  # .env variables
if not os.environ['BOT_TOKEN'] or not os.environ['API_KEY']:
    print('env variables not set correctly')
    quit(1)

bot_service = telebot.TeleBot(os.environ['BOT_TOKEN'])  # bot instance


class Bot:
    def __init__(self):
        self.prev_command = ''

    def handlers(self):

        @bot_service.message_handler(commands=['start', 'help'])
        def send_welcome(message):
            """Welcome message"""
            bot_service.send_message(message.chat.id, "Это бот, который поможет найти нужный фильм или сериал")

        @bot_service.message_handler(commands=['test'])
        def test_message(message):
            """test buttons"""
            markup = tt.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = tt.KeyboardButton("/start")
            item2 = tt.KeyboardButton("/help")
            markup.add(item1, item2)
            bot_service.send_message(message.chat.id, 'Выберите из меню', reply_markup=markup)

        @bot_service.message_handler(commands=['find'])
        def send_film_test(message):
            self.prev_command = 'find'
            bot_service.send_message(message.chat.id, "Напишите назавние искомого фильма или сериала")


        @bot_service.message_handler(func=lambda m: True)
        def echo_all(message):
            """Reply for any other message"""
            if self.prev_command == 'find':
                print(message.text)
                url = 'https://api.kinopoisk.dev/v1.2/movie/search'
                headers = {"X-API-KEY": os.environ["API_KEY"]}
                # params = {'id': 335}
                params = {'query': message.text}
                Fetch = FilmFetch(url, headers, params)

                try:
                    data = Fetch.cached_request()  # кэшированный запрос
                    bot_service.reply_to(message, f"По вашему запросу найдено {data['total']} результатов")

                    for info in data['docs']:
                        poster, caption = form_result(info)

                        bot_service.send_photo(message.chat.id, photo=poster, caption=caption)

                except Exception as e:
                    print("Request unsuccessful", e)

                finally:
                    self.prev_command = ''

            else:
                bot_service.reply_to(message, "Не понял :/")


if __name__ == "__main__":
    bot = Bot()
    bot.handlers()
    print("bot running")
    bot_service.infinity_polling()








