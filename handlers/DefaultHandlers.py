"""Welcome and help messages"""

from telegram import Update
from telegram.ext import ContextTypes


class DefaultHandlers:
    """Default commands handlers"""

    def __init__(self, logger, default_markup):
        self.logger = logger
        self.default_markup = default_markup

    async def send_welcome(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Message on '/start' """
        await update.message.reply_text(
            "Это бот, который поможет найти нужный фильм или сериал",
            reply_markup=self.default_markup
        )

    async def send_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Message on '/help' """

        await update.message.reply_text(
            "Вот команды которые вы можете использовать:\n"
            "/find - находит фильмы по названию\n"
            "/random - находит случайный фильм\n"
            "/actor - находит фильмы по актеру\n"
            "/category - находит фильмы по категориям",
            reply_markup=self.default_markup
        )
