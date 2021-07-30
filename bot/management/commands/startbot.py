from django.core.management.base import BaseCommand, CommandError
import os
import telebot

class Command(BaseCommand):
    help = 'Start telegram bot daemon'

    # def add_arguments(self, parser):
    #     parser.add_argument('typeapp', nargs='+', type=str)

    def handle(self, *args, **options):
        key = os.getenv('APP_KEY')
        bot = telebot.TeleBot(key)

        self.stdout.write(self.style.SUCCESS('Start telegram bot'))

        @bot.message_handler(commands=['start'])
        def start(message):
            orderText = message.text
            userId = message.chat.id
            print(message)
            bot.send_message(
                message.chat.id, 'Ваш заказ в готовится. Ожидайте. Я сообщу, когда его можно будет забрать')
        
        bot.polling()
        # bot.send_message(321486086, 'я могу написать себе')
            # try:
            #     poll = Poll.objects.get(pk=poll_id)
            # except Poll.DoesNotExist:
            #     raise CommandError('Poll "%s" does not exist' % poll_id)
