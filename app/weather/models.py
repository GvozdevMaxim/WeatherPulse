from django.db import models
from django.conf import settings

class City(models.Model):
    name = models.CharField(max_length=100, unique=True)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}, {self.country}"

    class Meta:
        ordering = ['name', 'country']

class WeatherHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    temperature = models.FloatField(null=True, blank=True)
    humidity = models.IntegerField(null=True, blank=True)
    pressure = models.IntegerField(null=True, blank=True)
    wind_speed = models.FloatField(null=True, blank=True)
    cloudiness = models.IntegerField(null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated_at']
        unique_together = ('user', 'city', 'updated_at')
        indexes = [
            models.Index(fields=['city']),
            models.Index(fields=['user']),
            models.Index(fields=['-updated_at']),
        ]
        get_latest_by = 'updated_at'
        constraints = [
            models.UniqueConstraint(fields=['user', 'city', 'updated_at'], name='unique_user_city_time')
        ]

    def __str__(self):
        return