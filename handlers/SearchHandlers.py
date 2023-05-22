"""Film searching module"""

from telegram import ReplyKeyboardMarkup, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from utils.fetch import FilmFetch


def make_film_card(info):
    """Forms a card response"""
    print(info)
    poster = info['poster']['url']

    caption = f"Фильм: {info['name']}\n" \
              f"Рейтинг: {info['rating']['kp']}\n" \
              f"Год: {info['year']}\n\n" \
              f"{info['description']}"

    markup_buttons = [[InlineKeyboardButton("Просмотреть рецензию", callback_data=info['id'])]]
    if info['externalId']['kpHD'] is not None:
        markup_buttons.append([InlineKeyboardButton(
            text='Смотреть онлайн',
            url=f"https://hd.kinopoisk.ru/film/{info['externalId']['kpHD']}")])

    markup = InlineKeyboardMarkup(markup_buttons)

    return poster, caption, markup


class SearchHandlers:
    """Search commands handlers"""

    def __init__(self, states, logger):
        self.logger = logger
        self.states = states

    async def send_film(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Prompt a name"""
        await update.message.reply_text(
            "Напишите название фильма или сериала",
            reply_markup=ReplyKeyboardMarkup([['/cancel']])
        )
        self.logger.info("SENT reply with state {FIND_BY_NAME}")
        return self.states.FIND_BY_NAME

    async def response_film(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Reply for film find"""
        url = 'https://api.kinopoisk.dev/v1.3/movie'
        # params = {'id': 335}
        params = {'name': update.message.text, 'limit': '3'}
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

        except Exception:  # pylint: disable=W
            self.logger.error("ERROR occurred:")

    async def send_actor(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Prompt for a name of the actor"""
        await update.message.reply_text(
            "Какого актёра вы хотите найти?",
            reply_markup=ReplyKeyboardMarkup([['/cancel']])
        )
        self.logger.info("SENT reply with state {FIND_BY_ACTOR}")
        return self.states.FIND_BY_ACTOR

    async def response_actor(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Reply for film find"""
        url = 'https://api.kinopoisk.dev/v1.3/movie'
        # params = {'id': 335}
        params = {'persons.name': update.message.text, 'limit': '3'}
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

        except Exception:  # pylint: disable=W
            self.logger.error("ERROR occurred:")

    async def review_callback(self, update: Update, context):
        """Reply for review find"""
        query = update.callback_query
        url = "https://api.kinopoisk.dev/v1/review"
        params = {'movieId': query.data, 'limit': '1'}
        Fetch = FilmFetch(url, params)
        try:
            data = Fetch.cached_request()

            for info in data['docs']:
                await query.message.reply_text(info['review'], parse_mode="html")

        except Exception:
            self.logger.error("SOME ERROR OCCURED")
        print('Просматривается отзыв для фильма с номером:', query.data)
        await query.answer()
