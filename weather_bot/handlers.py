import logging
from telegram import Update
from telegram.ext import ContextTypes
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async
from app.subscriptions.models import UserSubscription
from app.weather.models import WeatherHistory

logger = logging.getLogger(__name__)
User = get_user_model()


async def weather_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tg_user_id = update.effective_user.id

    try:
        user = await sync_to_async(User.objects.get)(telegram_id=tg_user_id)
    except User.DoesNotExist:
        await update.message.reply_text("Вы не привязаны к системе. Обратитесь к администратору.")
        return
    except Exception:
        logger.error("Ошибка при получении пользователя по telegram_id %s", tg_user_id, exc_info=True)
        await update.message.reply_text("Произошла ошибка при поиске вашего профиля. Попробуйте позже.")
        return

    try:
        subs = await sync_to_async(list)(UserSubscription.objects.filter(user=user))
    except Exception:
        logger.error("Ошибка при получении подписок пользователя %s", user.id, exc_info=True)
        await update.message.reply_text("Не удалось получить ваши подписки. Попробуйте позже.")
        return

    if not subs:
        await update.message.reply_text("У вас нет активных подписок.")
        return

    messages = []
    for sub in subs:
        try:
            city = await sync_to_async(getattr)(sub, 'city')
            last_weather_qs = WeatherHistory.objects.filter(user=user, city=city).order_by('-updated_at')
            last_weather = await sync_to_async(last_weather_qs.first)()
            if not last_weather:
                continue

            messages.append(
                f"Город: {city.name}\n"
                f"Температура: {last_weather.temperature}°C\n"
                f"Влажность: {last_weather.humidity}%\n"
                f"Ветер: {last_weather.wind_speed} м/с\n"
                f"Давление: {last_weather.pressure} гПа\n"
                f"Облачность: {last_weather.cloudiness}%\n"
                f"Обновлено: {last_weather.updated_at.strftime('%Y-%m-%d %H:%M')}"
            )
        except Exception:
            logger.error(
                "Ошибка при обработке подписки пользователя %s, города %s",
                user.id, sub.city_id, exc_info=True
            )
            await update.message.reply_text(
                f"Не удалось получить данные по городу {getattr(sub.city, 'name', 'неизвестному')}.")

    if messages:
        await update.message.reply_text("\n\n".join(messages))
    else:
        await update.message.reply_text("Нет данных о погоде.")
