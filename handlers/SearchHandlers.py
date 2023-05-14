import telebot.types as tt
from utils.fetch import *


def make_film_card(info):
    print(info)
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

    return poster, caption, markup


class SearchHandlers:
    def __init__(self, bot_service):
        self.bot_service = bot_service

    def set_handlers(self):
        @self.bot_service.message_handler(commands=['find'])
        def send_film_test(message):
            """Film searching"""
            self.prev_command = 'find'
            self.bot_service.send_message(
                message.chat.id,
                "Напишите название искомого фильма или сериала",
                reply_markup=tt.ReplyKeyboardRemove()
            )

        @self.bot_service.message_handler(text=['film'])
        def response_film(message):
            """Reply for any other message"""
            print(message.text)
            url = 'https://api.kinopoisk.dev/v1.2/movie/search'

            params = {'id': 335}
            # params = {'query': message.text}
            Fetch = FilmFetch(url, params)
            try:
                data = Fetch.cached_request()
                self.bot_service.reply_to(
                    message,
                    f"По вашему запросу найдено {data['total']} результатов"
                )

                for info in data['docs']:
                    poster, caption, markup = make_film_card(info)

                    self.bot_service.send_photo(
                        message.chat.id,
                        photo=poster,
                        caption=caption,
                        reply_markup=markup
                    )

            except Exception as e:
                print("Request unsuccessful", e)
