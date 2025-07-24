from django.contrib import admin
from .models import City, WeatherHistory


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')
    search_fields = ('name', 'country')
    ordering = ('name', 'country')


@admin.register(WeatherHistory)
class WeatherHistoryAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'city',
        'temperature',
        'humidity',
        'pressure',
        'wind_speed',
        'cloudiness',
        'updated_at',
    )
    list_filter = ('city', 'user', 'updated_at')
    search_fields = (
        'user__username',
        'city__name',
        'description',
    )
    ordering = ('-updated_at',)
    date_hierarchy = 'updated_at'
