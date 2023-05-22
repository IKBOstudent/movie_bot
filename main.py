"""telegram movie bot"""

import os
import sys
import logging
from dotenv import load_dotenv

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, \
    filters, ConversationHandler, CallbackQueryHandler

from handlers.SearchHandlers import SearchHandlers
from handlers.TestHandlers import TestHandlers
from handlers.DefaultHandlers import DefaultHandlers

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


class STATES:
    """states for conversations"""
    START = 0
    FIND_BY_NAME = 1
    FIND_REVIEWS = 2
    FIND_BY_ACTOR = 3


default_markup = ReplyKeyboardMarkup([
    ['/find', '/help', '/actor'],
    ['/test_keyboard']
], resize_keyboard=True)

default = DefaultHandlers(logger, default_markup)
test = TestHandlers(logger)
search = SearchHandlers(STATES, logger)


async def keyboard_callback(update, context):
    query = update.callback_query
    # print('query:', query)

    print('query.data:', query.data)
    query.answer(f'selected: {query.data}')


application.add_handler(CommandHandler("start", default.send_welcome))
application.add_handler(CommandHandler("help", default.send_help))
application.add_handler(CommandHandler("test_keyboard", test.test_keyboard))
#application.add_handler(CallbackQueryHandler(keyboard_callback))


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancels conversation"""
    await update.effective_user.send_message('Canceled', reply_markup=default_markup)
    return ConversationHandler.END


conv_handler = ConversationHandler(
    entry_points=[CommandHandler('find', search.send_film)],
    states={
        STATES.START: [],
        STATES.FIND_BY_NAME: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, search.response_film),
            CallbackQueryHandler(search.review_callback)
        ],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)

application.add_handler(conv_handler)

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('actor', search.send_actor)],
    states={
        STATES.START: [],
        STATES.FIND_BY_ACTOR: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, search.response_actor),
        ],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)

application.add_handler(conv_handler)


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
