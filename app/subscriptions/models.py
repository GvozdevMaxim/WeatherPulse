from django.db import models
from django.conf import settings
from app.weather.models import City


class UserSubscription(models.Model):
    ALERT_DIRECTION_CHOICES = [
        ('above', 'Выше порога'),
        ('below', 'Ниже порога'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE
    )

    # Подписанные параметры
    temperature = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    humidity = models.PositiveIntegerField(
        blank=True,
        null=True
    )
    pressure = models.PositiveIntegerField(
        blank=True,
        null=True
    )
    wind_speed = models.FloatField(
        blank=True,
        null=True
    )
    cloudiness = models.PositiveIntegerField(
        blank=True,
        null=True
    )
    description = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    # Пороговые значения и направления
    temperature_threshold = models.FloatField(
        blank=True,
        null=True
    )
    temperature_alert_direction = models.CharField(
        max_length=5,
        choices=ALERT_DIRECTION_CHOICES,
        default='above'
    )

    humidity_threshold = models.PositiveIntegerField(
        blank=True,
        null=True
    )
    pressure_threshold = models.PositiveIntegerField(
        blank=True,
        null=True
    )
    wind_speed_threshold = models.FloatField(
        blank=True,
        null=True
    )

    notified = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'city')
        ordering = ['user', 'city']

    def __str__(self):
        return f'{self.user} subscribed to {self.city}'
