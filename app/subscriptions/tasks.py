from celery import shared_task
from .models import UserSubscription
from app.weather.models import WeatherHistory
from ..weather.utils import fetch_weather_data
from django.core.mail import send_mail


@shared_task(name="app.subscriptions.tasks.update_weather_data")
def update_weather_data():
    """Обновляет данные о погоде проходясь по всем подпискам в базе"""
    subscriptions = UserSubscription.objects.select_related('user', 'city').all()

    for sub in subscriptions:
        data = fetch_weather_data(sub.city.name)
        if data:
            sub.temperature = data['temperature']
            sub.humidity = data['humidity']
            sub.pressure = data['pressure']
            sub.wind_speed = data['wind_speed']
            sub.cloudiness = data['cloudiness']
            sub.description = data['description']
            sub.save()

            WeatherHistory.objects.create(
                user=sub.user,
                city=sub.city,
                temperature=sub.temperature,
                humidity=sub.humidity,
                pressure=sub.pressure,
                wind_speed=sub.wind_speed,
                cloudiness=sub.cloudiness,
                description=sub.description,
            )

            check_weather_threshold.delay(sub.id)


@shared_task(name="app.subscriptions.tasks.check_weather_threshold")
def check_weather_threshold(subscription_id):
    """Отправляет пользователю письмо на почту в случае если температура/влажность/скорость ветра вышла за границу (threshold) указанную при подписке"""
    try:
        sub = UserSubscription.objects.select_related('user', 'city').get(id=subscription_id)
    except UserSubscription.DoesNotExist:
        print(f"⚠ Подписка {subscription_id} не найдена")
        return

    email_data = []

    def safe_float(value):
        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    temp = safe_float(sub.temperature)
    threshold = safe_float(sub.temperature_threshold)

    if threshold is not None and temp is not None:
        if sub.temperature_alert_direction == 'above' and temp > threshold:
            email_data.append(f"Температура: {temp}°C поднялась выше порога: {threshold}°C")
        elif sub.temperature_alert_direction == 'below' and temp < threshold:
            email_data.append(f" Температура: {temp}°C опустилась ниже порога {threshold}°C")

    if sub.humidity_threshold is not None and sub.humidity is not None:
        if sub.humidity > sub.humidity_threshold:
            email_data.append(f"Влажность: {sub.humidity}% (порог: {sub.humidity_threshold}%)")

    if sub.pressure_threshold is not None and sub.pressure is not None:
        if sub.pressure > sub.pressure_threshold:
            email_data.append(f"Давление: {sub.pressure} hPa (порог: {sub.pressure_threshold} hPa)")

    if sub.wind_speed_threshold is not None and sub.wind_speed is not None:
        if sub.wind_speed > sub.wind_speed_threshold:
            email_data.append(f"Скорость ветра: {sub.wind_speed}м/с (порог: {sub.wind_speed_threshold}м/с)")

    if email_data and not sub.notified:
        subject = f"⚠Погода в {sub.city.name} превысила установленные пороги"
        message = "Обнаружены следующие превышения:\n\n" + "\n".join(email_data)

        send_mail(
            subject,
            message,
            'noreply@weatherpulse.com',
            [sub.user.email],
            fail_silently=False,
        )

        print(f"Уведомление отправлено {sub.user.email} для {sub.city.name}")
        sub.notified = True
        sub.save()

    if not email_data and sub.notified:
        sub.notified = False
        sub.save()
        print(f" Сброс уведомления для {sub.user.email}")
