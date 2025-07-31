from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import UserSubscription
from .serializers import UserSubscriptionSerializer
from app.weather.utils import fetch_weather_data


class UserSubscriptionViewSet(viewsets.ModelViewSet):
    queryset = UserSubscription.objects.all()
    serializer_class = UserSubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # При генерации swagger документации возвращаем пустой queryset
        if getattr(self, 'swagger_fake_view', False):
            return self.queryset.none()

        user = self.request.user
        # Если пользователь анонимный, тоже возвращаем пустой queryset,
        # чтобы не вызывать ошибку в фильтре
        if user.is_anonymous:
            return self.queryset.none()

        return self.queryset.filter(user=user)

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
