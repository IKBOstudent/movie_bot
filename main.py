
from flask import Flask, request
import os
import sys
from dotenv import load_dotenv
import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Application, TypeHandler, CommandHandler, CallbackContext, ContextTypes, MessageHandler, \
    filters, ExtBot, CallbackQueryHandler, ConversationHandler

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
    START = 0
    FIND_BY_NAME = 1


default_markup = ReplyKeyboardMarkup([
            ['/find', '/help'],
            ['/test_keyboard']
        ], resize_keyboard=True)

default = DefaultHandlers(logger, default_markup)
test = TestHandlers(logger)
search = SearchHandlers(STATES, logger)


application.add_handler(CommandHandler("start", default.send_welcome))
application.add_handler(CommandHandler("help", default.send_help))
application.add_handler(CommandHandler("test_keyboard", test.test_keyboard))


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_user.send_message('Canceled', reply_markup=default_markup)
    return ConversationHandler.END


conv_handler = ConversationHandler(
    entry_points=[CommandHandler('find', search.send_film)],
    states={
        STATES.START: [],
        STATES.FIND_BY_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, search.response_film)],
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





