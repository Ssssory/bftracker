from datetime import datetime, date
import os
from server.models import Client, Order, Point
from bot.helper.messages import Messages
import telebot
import base64
import json
from django.conf import settings

from server.classes.status import Status

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
            today = date.today()
            order = Order.objects.get(point=point_id, order_id=order_id, created_at__gt=today)
            client = Client.objects.get(messenger_id=userId, messenger_type="telegram")
            if not client:
                newClient = Client()
                newClient.messenger_id = userId
                newClient.messenger_type = "telegram"
                newClient.save()
                order.client = newClient
            else:
                order.client = client
            order.save()
        except Exception as e:
            print("error: order not fount")
            print(str(e))
            self.send_message(userId, "Обнаружена проблема, пожалуйста, сообщите администратору")
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

    def send_status_message(self, client, status):
        id = client.messenger_id
        if status == Status.CALL:
            self.send_message(id, Messages.default_call_text)
        if status == Status.READY:
            self.send_message(id, Messages.default_ready_text)

    def getParam(self, msg):
        print('-------------')
        msg = msg.replace("/start ", "")
        msg += "=" * ((4 - len(msg) % 4) % 4)
        orderText = base64.b64decode(msg).decode('utf-8')
        data = json.loads(orderText)
        print(orderText)
        print('-------------')
        return data
