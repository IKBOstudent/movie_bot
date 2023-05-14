from telegram import ReplyKeyboardMarkup, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, ConversationHandler
from utils.fetch import *


def make_film_card(info):
    print(info)
    poster = info['poster']['url']

    caption = f"Фильм: {info['name']}\n" \
              f"Рейтинг: {info['rating']['kp']}\n" \
              f"Год: {info['year']}\n\n" \
              f"{info['description']}"

    markup_buttons = []
    if info['externalId']['kpHD'] is not None:
        markup_buttons.append([InlineKeyboardButton(
            text='Смотреть онлайн',
            url=f"https://hd.kinopoisk.ru/film/{info['externalId']['kpHD']}")])

    markup = InlineKeyboardMarkup(markup_buttons)

    return poster, caption, markup


class SearchHandlers:
    def __init__(self, states, logger):
        self.logger = logger
        self.states = states

    async def send_film(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "Напишите название фильма или сериала",
            reply_markup=ReplyKeyboardMarkup([['/cancel']])
        )
        self.logger.info("SENT reply with state {FIND_BY_NAME}")
        return self.states.FIND_BY_NAME

    async def response_film(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Reply for any other message"""
        url = 'https://api.kinopoisk.dev/v1/movie'
        params = {'id': 335}
        # params = {'query': message.text}
        Fetch = FilmFetch(url, params)
        try:
            data = Fetch.cached_request()

            await update.message.reply_text(
                f"По вашему запросу найдено результатов: {data['total']}"
            )

            for info in data['docs']:
                poster, caption, markup = make_film_card(info)

                await update.message.reply_photo(
                    photo=poster,
                    caption=caption,
                    reply_markup=markup
                )

        except Exception as e:
            self.logger.error("ERROR occurred:")

        finally:
            self.logger.info("Ended conversation")
            return ConversationHandler.END
