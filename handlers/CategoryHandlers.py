from telegram import ReplyKeyboardMarkup, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler, CallbackContext
from utils.fetch import FilmFetch
from telegram import InputMediaPhoto
"""Film categories module"""
global_page = 0
glob_categ = []
current_categ = ""


def make_film_card(info):
    """Forms a card response"""
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
            url=f"https://hd.kinopoisk.ru/film/{info['externalId']['kpHD']}"),
            InlineKeyboardButton(text="Назад", callback_data="return2")])

    markup = InlineKeyboardMarkup(markup_buttons)

    return poster, caption, markup


async def response_film_by_id(update, id):
    url = 'https://api.kinopoisk.dev/v1/movie'
    params = {'id': id}
    Fetch = FilmFetch(url, params)
    try:

        data = Fetch.cached_request()
        for info in data['docs']:
            poster, caption, markup = make_film_card(info)
            query = update.callback_query

            photo_url = InputMediaPhoto(poster)
            await query.edit_message_text(text=caption)
            await query.edit_message_reply_markup(reply_markup=markup)
            await query.edit_message_media(media=photo_url)


    except:
        pass


def createButtons(info):
    """Creating buttons of categories"""
    caption = "Жанры:"
    global global_page
    global_page = 1
    if info is not None:
        category_buttons = []
        tmp_arr_btn = []
        for category in info:
            tmp_arr_btn.append(InlineKeyboardButton(text=category['name'], callback_data=category['name']))
            if len(tmp_arr_btn) == 3:
                category_buttons.append(tmp_arr_btn)
                tmp_arr_btn = []
        category_buttons.append(tmp_arr_btn)
        markup = InlineKeyboardMarkup(category_buttons)
        return caption, markup


def createBtnFilms(info):
    """Creating buttons of films and switches"""
    caption = "Выберите фильм"
    next_back_button = []
    if info is not None:
        film_buttons = []
        for film in info['docs']:
            film_buttons.append(
                [InlineKeyboardButton(text=film['name'] + " " + str(film['year']), callback_data=film['id'])])
        if global_page != 1:
            next_back_button = [InlineKeyboardButton(text="<-", callback_data="back"),
                                InlineKeyboardButton(text="->", callback_data="next")]
        elif global_page == 1:
            next_back_button = [InlineKeyboardButton(text="->", callback_data="next")]

        return_button = [InlineKeyboardButton(text="return", callback_data="return")]
        """Update message and show films"""
        film_buttons.append(next_back_button)
        film_buttons.append(return_button)
        markup = InlineKeyboardMarkup(film_buttons)
        return caption, markup


async def response_film_by_categ(update, page, category_data):
    """Response film by categories"""
    url = 'https://api.kinopoisk.dev/v1/movie'
    params = {"page": page, "genres.name": category_data}
    Fetch = FilmFetch(url, params)
    try:
        data = Fetch.cached_request()
        caption, markup = createBtnFilms(data)

        query = update.callback_query
        await query.edit_message_text(text=caption)
        await query.edit_message_reply_markup(reply_markup=markup)
    except:
        pass


async def buttonFilmHandler(update: Update,context: ContextTypes.DEFAULT_TYPE):
    """Handler of all buttons"""
    query = update.callback_query
    data = query.data
    global global_page, current_categ
    for categ in glob_categ:
        if data == categ['name']:
            current_categ = data
            await response_film_by_categ(update, global_page, current_categ)

    if data == "return":
        """Return from list of films to categories"""
        caption, markup = createButtons(glob_categ)
        query = update.callback_query
        await query.edit_message_text(text=caption)
        await query.edit_message_reply_markup(reply_markup=markup)

    elif global_page != 1 and data == "back":
        """Go to next previos page of films"""
        global_page -= 1
        await response_film_by_categ(update, global_page, current_categ)
    elif data == "next":
        """Go to next page of films"""
        global_page += 1
        await response_film_by_categ(update, global_page, current_categ)
    elif data == "return2":
        """Return from film to list of films"""
        await response_film_by_categ(update, global_page, current_categ)
    elif data.isdigit() == True:
        data = int(data)
        await response_film_by_id(update, data)


class CategoryHandler:
    def __init__(self, state,logger):
        self.logger = logger
        self.state = state

    async def response_categories(self, update: Update,context: ContextTypes.DEFAULT_TYPE):
        """Response y categories"""
        global glob_categ
        url = 'https://api.kinopoisk.dev/v1/movie/possible-values-by-field'
        params = {"field": "genres.name"}
        Fetch = FilmFetch(url, params)
        try:
            data = Fetch.cached_request()
            glob_categ = data
            caption, markup = createButtons(data)
            """Update message and categories"""
            await update.message.reply_text(
                text=caption,
                reply_markup=markup
            )
        except:
            pass
