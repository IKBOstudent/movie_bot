import telebot.types as tt


class DefaultHandlers:
    def __init__(self, bot_service):
        self.bot_service = bot_service
        self.default_markup = tt.ReplyKeyboardMarkup(True, True)
        self.default_markup.row('/find', '/dice')
        self.default_markup.row('/aaa', '/bbb')
        self.default_markup.row('/test_keyboard')

    def set_handlers(self):
        @self.bot_service.message_handler(commands=['start', 'help'])
        def send_welcome(message):
            """Welcome message"""
            self.bot_service.send_message(
                message.chat.id,
                "Это бот, который поможет найти нужный фильм или сериал",
                reply_markup=self.default_markup
            )

        @self.bot_service.message_handler(commands=['dice'])
        def send_dice(message):
            """Dice"""
            self.bot_service.send_dice(message.chat.id)
