from django.core.management import BaseCommand

from bot.management.commands.bot_manager import BotManager
from config.config import TELEGRAM_API


class Command(BaseCommand):
    help = "TG Bot to set and maintain goals"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('БОТ ЗАПУЩЕН!'))
        bot_manager = BotManager(TELEGRAM_API)
        bot_manager.run_bot()

        self.stdout.write(self.style.SUCCESS('БОТ ВЫКЛЮЧЕН'))