import logging
from django.core.management.base import BaseCommand
from bot.bot import bot
from django.utils import timezone


class Command(BaseCommand):
    help = 'Starts the Telegram bot'

    def handle(self, *args, **options):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        start_time = timezone.now()
        logging.info(f'Telegram bot started at {start_time}')
        bot.polling()
        end_time = timezone.now()
        logging.info(f'Telegram bot stopped at {end_time}')
