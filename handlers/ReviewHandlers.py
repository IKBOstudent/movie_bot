"""Review searching module"""

from telegram import ReplyKeyboardMarkup, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from utils.fetch import FilmFetch


def make_review_card(info):
    """Forms a card response for the review"""
    print(info)



class ReviewHandlers:
    """Search for review commands handlers"""
    def __init__(self, states, logger):
        self.logger = logger
        self.states = states

    async def send_review(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Ask for a name"""
        await update.message.reply_text(
            "Для какого фильма искать отзывы?",
            reply_markup=ReplyKeyboardMarkup([["/cancel"]])
        )
        self.logger.info("SENT reply with state {FIND_REVIEWS}")
        return self.states.FIND_REVIEWS

    async def response_review(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Reply for a reviews find"""
        url = "https://api.kinopoisk.dev/v1/review"
        params = {'id'}