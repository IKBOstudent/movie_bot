"""Test handlers"""

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes


class TestHandlers:
    """Test handlers"""
    
    def __init__(self, logger):
        self.logger = logger

    async def test_keyboard(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """test buttons"""
        markup = ReplyKeyboardMarkup(
            [
                ["/start"],
                ["/help"]
            ],
            one_time_keyboard=True,
            resize_keyboard=True
        )
        await update.message.reply_text("Выберите из меню", reply_markup=markup)
