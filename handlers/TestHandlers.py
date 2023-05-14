import telebot.types as tt


class TestHandlers:
    def __init__(self, bot_service):
        self.bot_service = bot_service

    def set_handlers(self):
        @self.bot_service.message_handler(commands=['test_keyboard'])
        def test_message(message):
            """test buttons"""
            markup = tt.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = tt.KeyboardButton("/start")
            item2 = tt.KeyboardButton("/help")
            markup.add(item1, item2)
            self.bot_service.send_message(message.chat.id, 'Выберите из меню', reply_markup=markup)
