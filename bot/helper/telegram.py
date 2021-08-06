import os
from bot.helper.messages import Messages
import telebot

class TelegramServise():
    bot = None

    def __init__(self):
        key = os.getenv('APP_KEY')

        if(self.bot is None):
            bot = telebot.TeleBot(key)

            self.bot = bot
    
    def start(self, message):
        orderText = message.text
        userId = message.chat.id
        text = Messages.default_start_text
        # print(message)
        self.send_message(userId, text)

    def send_message(self, id, text):
        self.bot.send_message(id, text)
