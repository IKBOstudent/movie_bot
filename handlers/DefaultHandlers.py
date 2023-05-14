from telegram import ForceReply, Update, ReplyKeyboardMarkup
from telegram.ext import CommandHandler, ContextTypes, MessageHandler, filters, ConversationHandler


class DefaultHandlers:
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
        # TODO
