"""Search by category handlers"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
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

    markup_buttons.append([InlineKeyboardButton(text="Назад", callback_data="film return")])
    markup = InlineKeyboardMarkup(markup_buttons)

    return poster, caption, markup


class CategoryHandler:
    """Search by categories"""
    def __init__(self, state, logger):
        self.logger = logger
        self.state = state
        self.current_page = 1
        self.all_categ = []
        self.current_categ = ''

    def createButtons(self, info):
        """Creating buttons of categories"""

        category_buttons = []
        tmp_arr_btn = []
        for category in info:
            tmp_arr_btn.append(InlineKeyboardButton(
                category['name'],
                callback_data=f"categ {category['name']}"
            ))
            if len(tmp_arr_btn) == 3:
                category_buttons.append(tmp_arr_btn)
                tmp_arr_btn = []
        category_buttons.append(tmp_arr_btn)
        category_buttons.append([InlineKeyboardButton('Отмена', callback_data="cancel")])
        markup = InlineKeyboardMarkup(category_buttons)
        return markup

    async def response_categories(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Response by categories"""
        url = 'https://api.kinopoisk.dev/v1/movie/possible-values-by-field'
        params = {"field": "genres.name"}
        Fetch = FilmFetch(url, params)
        try:
            data = Fetch.cached_request()
            self.all_categ = data

            caption = "Жанры:"
            markup = self.createButtons(data)

            await update.message.reply_text(
                text=caption,
                reply_markup=markup
            )

            return self.state.FIND_CATEGORY

        except Exception:  # pylint: disable=W
            self.logger.error("ERROR occurred:")

    def createBtnFilms(self, info):
        """Creating buttons of films and switches"""

        film_buttons = []
        for film in info['docs']:
            film_buttons.append(
                [InlineKeyboardButton(
                    film['name'] + " " + str(film['year']),
                    callback_data=f"film {film['id']}")]
            )

        if self.current_page != 1:
            film_buttons.append([InlineKeyboardButton(text="<-", callback_data="prev"),
                                    InlineKeyboardButton(text="->", callback_data="next")])
        elif self.current_page == 1:
            film_buttons.append([InlineKeyboardButton(text="->", callback_data="next")])

        film_buttons.append([InlineKeyboardButton(text="Назад", callback_data="categ return")])
        film_buttons.append([InlineKeyboardButton('Отмена', callback_data="cancel")])
        markup = InlineKeyboardMarkup(film_buttons)
        return markup

    async def response_film_by_categ(self, update: Update):
        """Response film by categories"""
        url = 'https://api.kinopoisk.dev/v1/movie'
        params = {"page": self.current_page, "genres.name": self.current_categ}
        Fetch = FilmFetch(url, params)
        try:
            data = Fetch.cached_request()
            caption = "Выберите фильм"

            markup = self.createBtnFilms(data)

            query = update.callback_query
            await query.edit_message_text(text=caption)
            await query.edit_message_reply_markup(reply_markup=markup)

        except Exception:  # pylint: disable=W
            self.logger.error("ERROR occurred:")

    async def response_film_by_id(self, update: Update, film_id):
        """Response film card"""
        url = 'https://api.kinopoisk.dev/v1.3/movie'
        params = {'id': film_id}
        Fetch = FilmFetch(url, params)
        try:
            data = Fetch.cached_request()
            _, caption, markup = make_film_card(data['docs'][0])

            query = update.callback_query
            # await query.edit_message_media(media=InputMediaPhoto(poster))
            await query.edit_message_text(text=caption, reply_markup=markup)

        except Exception:  # pylint: disable=W
            self.logger.error("ERROR occurred:")

    async def categ_callback(self, update: Update, context):
        """Handler of all buttons"""
        data = update.callback_query.data

        if data == "cancel":
            await update.callback_query.message.reply_text("Действие отменено")
            return ConversationHandler.END

        if data == "categ return":
            caption = "Жанры:"
            markup = self.createButtons(self.all_categ)
            query = update.callback_query
            await query.edit_message_text(text=caption, reply_markup=markup)

        elif data == "film return":
            # Return from film to list of films
            await self.response_film_by_categ(update)

        elif data.startswith("categ"):
            self.current_categ = data.split()[1]
            await self.response_film_by_categ(update)

        elif data.startswith("film"):
            await self.response_film_by_id(update, data.split()[1])

        elif self.current_page != 1 and data == "prev":
            # Go to next previous page of films
            self.current_page -= 1
            await self.response_film_by_categ(update)

        elif data == "next":
            # Go to next page of films
            self.current_page += 1
            await self.response_film_by_categ(update)
