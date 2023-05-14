from flask import Flask, request
import os
import sys
import telebot
import telebot.types as tt
from dotenv import load_dotenv
import logging


from handlers.SearchHandlers import SearchHandlers
from handlers.TestHandlers import TestHandlers
from handlers.DefaultHandlers import DefaultHandlers


load_dotenv()

try:
    os.environ['BOT_TOKEN'], os.environ['API_KEY']
except KeyError as e:
    print('Error with env variables', e)
    sys.exit("ENV ERROR")

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)


TOKEN = os.environ['BOT_TOKEN']


bot_service = telebot.TeleBot(TOKEN, threaded=False)

DefaultHandlers(bot_service).set_handlers()
TestHandlers(bot_service).set_handlers()
SearchHandlers(bot_service).set_handlers()


@bot_service.message_handler(func=lambda m: True)
def echo_all(message):
    """Reply for any other message"""
    bot_service.reply_to(message, "Не понял :/")


app = Flask(__name__)

if len(sys.argv) > 1 and sys.argv[1] == "PRODUCTION":
    DEPLOY_URL = 'https://movie-bot-5s64.onrender.com/'


    @app.route('/' + TOKEN, methods=['POST'])
    def getMessage():
        json_string = request.get_data().decode('utf-8')
        update = tt.Update.de_json(json_string)
        bot_service.process_new_updates([update])
        return "!", 200


    @app.route("/")
    def webhook():
        bot_service.remove_webhook()
        bot_service.set_webhook(url=DEPLOY_URL + TOKEN)
        return "!", 200


    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 8080)))
else:
    print("starting bot...")
    bot_service.infinity_polling()

