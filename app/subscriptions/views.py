from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import UserSubscription
from .serializers import UserSubscriptionSerializer
from app.weather.utils import fetch_weather_data



class UserSubscriptionViewSet(viewsets.ModelViewSet):
    """Вывод списка подписок"""
    queryset = UserSubscription.objects.all()
    serializer_class = UserSubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        city = serializer.validated_data['city']
        weather = fetch_weather_data(city.name)

        serializer.save(
            user=self.request.user,
            temperature=weather.get('temperature'),
            humidity=weather.get('humidity'),
            pressure=weather.get('pressure'),
            wind_speed=weather.get('wind_speed'),
            cloudiness=weather.get('cloudiness'),
            description=weather.get('description'),
        )
