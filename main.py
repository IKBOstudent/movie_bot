"""telegram movie bot"""

import os
import sys
import logging
from dotenv import load_dotenv

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, \
    filters, ConversationHandler, CallbackQueryHandler

from handlers.ActorHandlers import ActorHandlers
from handlers.FilmHandlers import FilmHandlers
from handlers.DefaultHandlers import DefaultHandlers
from handlers.CategoryHandlers import CategoryHandler

load_dotenv()

try:
    os.environ['BOT_TOKEN'], os.environ['API_KEY']
except KeyError as e:
    print('Error with env variables', e)
    sys.exit("ENV ERROR")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG
)
logger = logging.getLogger(__name__)

TOKEN = os.environ['BOT_TOKEN']

application = Application.builder().token(TOKEN).build()


class STATES_FILM:
    """states for conversations"""
    START = 0
    FIND_NAMES = 1


class STATES_ACTOR:
    START = 0
    FIND_ACTORS = 1


class STATES_CATEGORY:
    START = 0
    FIND_CATEGORY = 1


default_markup = ReplyKeyboardMarkup([
            ['/help', '/random'],
            ['/find', '/actor', '/category']
        ], resize_keyboard=True)

default = DefaultHandlers(logger, default_markup)
film = FilmHandlers(STATES_FILM, logger)
actor = ActorHandlers(STATES_ACTOR, logger)
category = CategoryHandler(STATES_CATEGORY, logger)

application.add_handler(CommandHandler("start", default.send_welcome))
application.add_handler(CommandHandler("help", default.send_help))
application.add_handler(CommandHandler("random", film.random_film))


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancels conversation"""
    await update.effective_user.send_message('Canceled', reply_markup=default_markup)
    return ConversationHandler.END


film_handler = ConversationHandler(
    entry_points=[CommandHandler('find', film.send_film)],
    states={
        STATES_FILM.START: [],
        STATES_FILM.FIND_NAMES: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, film.response_names),
            CallbackQueryHandler(film.film_callback)
        ]
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)

actor_handler = ConversationHandler(
    entry_points=[CommandHandler('actor', actor.send_actor)],
    states={
        STATES_ACTOR.START: [],
        STATES_ACTOR.FIND_ACTORS: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, actor.response_actors),
            CallbackQueryHandler(actor.actor_callback)
        ],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)

category_handler = ConversationHandler(
    entry_points=[CommandHandler('category', category.response_categories)],
    states={
        STATES_CATEGORY.START: [],
        STATES_CATEGORY.FIND_CATEGORY: [
            CallbackQueryHandler(category.categ_callback)
        ],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)

application.add_handler(film_handler)
application.add_handler(actor_handler)
application.add_handler(category_handler)


async def send_unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Unknown command or message handler"""
    await update.message.reply_text("Не понял :/")


application.add_handler(MessageHandler(filters.Regex(r'.*'), send_unknown))

if len(sys.argv) > 1 and sys.argv[1] == "PRODUCTION":
    pass
else:
    print("starting bot...")
    application.run_polling(drop_pending_updates=True)
    application.updater.initialize()
