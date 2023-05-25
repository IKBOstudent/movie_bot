"""Search by name handlers"""

from telegram import ReplyKeyboardMarkup, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from utils.fetch import FilmFetch


def make_film_card(info):
    """Forms a card response"""
    poster = info['poster']['url']

    caption = f"Фильм: {info['name']}\n" \
              f"Рейтинг: {info['rating']['kp']}\n" \
              f"Год: {info['year']}\n\n" \
              f"{info['description']}"

    markup_buttons = [[]]
    if info['externalId']['kpHD'] is not None:
        markup_buttons.append([InlineKeyboardButton(
            text='Смотреть онлайн',
            url=f"https://hd.kinopoisk.ru/film/{info['externalId']['kpHD']}")])

    markup = InlineKeyboardMarkup(markup_buttons)

    return poster, caption, markup


class ActorHandlers:
    """Search commands handlers"""

    def __init__(self, states, logger):
        self.logger = logger
        self.states = states
        self.cancel_button = [InlineKeyboardButton('Отмена', callback_data="cancel")]

    async def send_actor(self, update: Update, context):
        """Prompt for a name of the actor"""
        await update.message.reply_text(
            "Какого актёра вы хотите найти?",
            reply_markup=InlineKeyboardMarkup([self.cancel_button])
        )

        self.logger.info("SENT reply with state {FIND_ACTORS}")
        return self.states.FIND_ACTORS

    async def response_actors(self, update: Update, context):
        """Reply for film find"""
        url = 'https://api.kinopoisk.dev/v1/person'
        params = {'name': update.message.text}
        Fetch = FilmFetch(url, params)
        try:
            data = Fetch.cached_request()

            film_buttons = []
            for info in data['docs']:
                film_buttons.append(
                    [InlineKeyboardButton(
                        text=info['name'],
                        callback_data=f"{info['id']}")]
                )
            film_buttons.append(self.cancel_button)

            await update.message.reply_text(
                f"По вашему запросу найдено результатов: {data['total']}",
                reply_markup=InlineKeyboardMarkup(film_buttons)
            )

        except Exception:  # pylint: disable=W
            self.logger.error("ERROR occurred:")

    async def actor_callback(self, update: Update, context):
        """Reply for review find"""
        query = update.callback_query
        await query.answer()

        if query.data == "cancel":
            await query.message.reply_text("Действие отменено")
        else:
            url = "https://api.kinopoisk.dev/v1.3/movie"
            params = {'persons.id': query.data, 'limit': '3'}
            Fetch = FilmFetch(url, params)
            try:
                data = Fetch.cached_request()

                await query.delete_message()
                for info in data['docs']:
                    poster, caption, markup = make_film_card(info)

                    await query.message.reply_photo(
                        photo=poster,
                        caption=caption,
                        reply_markup=markup
                    )

            except Exception:  # pylint: disable=W
                self.logger.error("ERROR occurred:")

        return ConversationHandler.END