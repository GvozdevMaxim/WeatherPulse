from django.contrib import admin
from .models import UserSubscription


@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
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
