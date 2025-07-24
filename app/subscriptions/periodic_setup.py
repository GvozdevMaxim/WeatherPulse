import json
from django_celery_beat.models import IntervalSchedule, PeriodicTask


def setup_periodic_tasks():
    """Periodic tasks обновляет все данные о погоде на которые есть подписки в базе раз в час"""
    schedule, _ = IntervalSchedule.objects.get_or_create(
        every=1,
        period=IntervalSchedule.HOURS,
    )

    PeriodicTask.objects.get_or_create(
        interval=schedule,
        name='Update weather data every 1 Hour',
        task='app.subscriptions.tasks.update_weather_data',
        defaults={'enabled': True, 'args': json.dumps([])},
    )
