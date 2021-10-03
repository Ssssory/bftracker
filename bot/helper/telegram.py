import os
from server.models import Client, Order, Point
from bot.helper.messages import Messages
import telebot
import base64
import json
from django.conf import settings

class TelegramServise():
    bot = None

    def __init__(self):
        self.startBot()
        

    def startBot(self):
        if(self.bot is None):
            bot = telebot.TeleBot(settings.APP_KEY)
            self.bot = bot
    
    def start(self, message):
        try:
            data = self.getParam(message.text)
            point_id = data["point"]
            order_id = data["orderId"]
        except:
            print("error: can not decode" + message.text)
            return
        userId = message.chat.id

        point = Point.objects.get(pk=point_id)
        try:
            order = Order.objects.filter(point=point, order_id=order_id)
            client = Client.objects.filter(messenger_id=userId, messenger_type="telegram")
            if not client.exists():
                client = Client()
                client.messenger_id = userId
                client.messenger_type = "telegram"
                client.save()
            order.client = client
            order.save()
        except:
            print("error: order not fount")
            return

        text = Messages.default_start_text
        # print(message)
        self.send_message(userId, text)

    def send_message(self, id, text):
        try:
            self.bot.send_message(id, text)
        except:
            self.startBot()
            self.bot.send_message(id, text)

    def getParam(msg):
        print('-------------')
        print(msg)
        msg = msg.replace("/start ", "")
        print(msg)
        msg += "=" * ((4 - len(msg) % 4) % 4)
        print(msg)
        orderText = base64.b64decode(msg).decode('utf-8')
        print(orderText)
        data = json.loads(orderText)
        print(orderText)
        print('-------------')
        return data
