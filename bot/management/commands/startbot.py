from bot.helper.telegram import TelegramServise
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Start telegram bot daemon'

    # def add_arguments(self, parser):
    #     parser.add_argument('typeapp', nargs='+', type=str)

    def handle(self, *args, **options):
        service = TelegramServise()
        bot = service.bot

        self.stdout.write(self.style.SUCCESS('Start telegram bot'))

        @bot.message_handler(commands=['start'])
        def start(message):
            TelegramServise.start(service, message=message)
        
        bot.polling()
