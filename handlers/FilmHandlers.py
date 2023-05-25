"""Search by name handlers"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler
from utils.fetch import FilmFetch


def make_film_card(info):
    """Forms a card response"""
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

    return poster, caption, markup_buttons


class FilmHandlers:
    """Search commands handlers"""

    def __init__(self, states, logger):
        self.logger = logger
        self.states = states
        self.cancel_button = [InlineKeyboardButton('Отмена', callback_data="cancel")]

    async def random_film(self, update: Update, context):
        """Sends random film or episode"""
        url = "https://api.kinopoisk.dev/v1.3/movie/random"
        Fetch = FilmFetch(url, None)
        try:
            data = Fetch.standard_request()

            poster, caption, markup_buttons = make_film_card(data)
            print(caption)
            await update.message.reply_photo(
                photo=poster,
                caption=caption,
                reply_markup=InlineKeyboardMarkup(markup_buttons)
            )

        except Exception:  # pylint: disable=W
            self.logger.error("ERROR occurred:")

    async def send_film(self, update: Update, context):
        """Prompt a name"""

        await update.message.reply_text(
            "Начните писать название фильма или сериала",
            reply_markup=InlineKeyboardMarkup([self.cancel_button])
        )

        self.logger.info("SENT reply with state {FIND_NAMES}")
        return self.states.FIND_NAMES

    async def response_names(self, update: Update, context):
        """Reply for film find"""
        url = 'https://api.kinopoisk.dev/v1.3/movie'
        params = {'name': update.message.text}
        Fetch = FilmFetch(url, params)
        try:
            data = Fetch.cached_request()

            film_buttons = []
            for info in data['docs']:
                film_buttons.append(
                    [InlineKeyboardButton(
                        text=info['name'] + " " + str(info['year']),
                        callback_data=f"film {info['id']}")]
                )
            film_buttons.append(self.cancel_button)


            await update.message.reply_text(
                f"По вашему запросу найдено результатов: {data['total']}",
                reply_markup=InlineKeyboardMarkup(film_buttons)
            )

        except Exception:  # pylint: disable=W
            self.logger.error("ERROR occurred:")

    async def film_callback(self, update: Update, context):
        """Reply for film find"""
        query = update.callback_query
        await query.answer()

        if query.data == "cancel":
            await query.message.reply_text("Действие отменено")
            return ConversationHandler.END

        elif query.data.startswith("review"):
            url = "https://api.kinopoisk.dev/v1/review"
            params = {'movieId': query.data.split()[1], 'limit': '1'}
            Fetch = FilmFetch(url, params)
            try:
                data = Fetch.cached_request()
                info = data['docs'][0]
                await query.message.reply_text(info['review'])

            except Exception:  # pylint: disable=W
                self.logger.error("ERROR occurred:")
            return ConversationHandler.END

        elif query.data.startswith("film"):
            url = "https://api.kinopoisk.dev/v1.3/movie"
            params = {'id': query.data.split()[1]}
            Fetch = FilmFetch(url, params)
            try:
                info = Fetch.cached_request()['docs'][0]

                poster, caption, markup_buttons = make_film_card(info)

                markup_buttons.append(
                    [InlineKeyboardButton("Просмотреть рецензию", callback_data=f"review {info['id']}")])
                markup_buttons.append(
                    [InlineKeyboardButton('Отмена', callback_data="cancel")]
                )

                await query.delete_message()
                await query.message.reply_photo(
                    photo=poster,
                    caption=caption,
                    reply_markup=InlineKeyboardMarkup(markup_buttons)
                )

            except Exception:  # pylint: disable=W
                self.logger.error("ERROR occurred:")





