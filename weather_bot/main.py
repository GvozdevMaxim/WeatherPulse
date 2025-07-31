import os
import sys
import django
import logging
from telegram.ext import Application, CommandHandler
from weather_bot.config import BOT_TOKEN
from weather_bot.handlers import weather_handler


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WeatherPulse.settings')
django.setup()

logger = logging.getLogger(__name__)

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("weather", weather_handler))

    async def error_handler(update, context):
        logger.error("Произошла ошибка в обработчике Telegram бота", exc_info=context.error)

    app.add_error_handler(error_handler)

    app.run_polling()

if __name__ == "__main__":
    main()
