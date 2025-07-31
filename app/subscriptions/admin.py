from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import UserSubscription


@admin.register(UserSubscription)
class UserSubscriptionAdmin(ModelAdmin):
    list_display = (
        'user',
        'city',
        'temperature_threshold',
        'temperature_alert_direction',
        'notified',
    )
    list_filter = (
        'city',
        'notified',
        'temperature_alert_direction',
    )
    search_fields = (
        'user__username',
        'city__name',
        'description',
    )
    ordering = ('user', 'city')
