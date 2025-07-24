from rest_framework import serializers
from .models import UserSubscription

class UserSubscriptionSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    def validate_temperature_threshold(self, value):
        if value is not None and (value < -50 or value > 60):
            raise serializers.ValidationError("Порог температуры должен быть от -50 до 60 °C.")
        return value

    def validate_humidity_threshold(self, value):
        if value is not None and (value < 0 or value > 100):
            raise serializers.ValidationError("Порог влажности должен быть от 0 до 100%.")
        return value

    def validate_pressure_threshold(self, value):
        if value is not None and (value < 700 or value > 800):
            raise serializers.ValidationError("Порог давления должен быть от 700 до 800 hPa.")
        return value

    def validate_wind_speed_threshold(self, value):
        if value is not None and (value < 0 or value > 50):
            raise serializers.ValidationError("Порог скорости ветра должен быть от 0 до 50 м/с.")
        return value

    class Meta:
        model = UserSubscription
        fields = [
            'id',
            'user',
            'city',

            'temperature',
            'humidity',
            'pressure',
            'wind_speed',
            'cloudiness',
            'description',

            'temperature_alert_direction',
            'temperature_threshold',
            'humidity_threshold',
            'pressure_threshold',
            'wind_speed_threshold',
        ]
        read_only_fields = [
            'user',
            'temperature',
            'humidity',
            'pressure',
            'wind_speed',
            'cloudiness',
            'description',
        ]

