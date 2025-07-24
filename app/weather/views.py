import json
from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from .models import City, WeatherHistory
from .serializers import CitySerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [AllowAny]



def weather_chart_view(request, city_id):
    """Представление для отрисовки шаблона с графиком погоды в браузере
    (реализованно исключительно для наглядности)"""
    User = get_user_model()
    metric = request.GET.get('metric', 'temperature')
    user = request.user

    if not user.is_authenticated:
        # Например, fallback на гостевого пользователя или обработка ошибки
        user = User.objects.get(username='gastinhaha')
    history = list(WeatherHistory.objects.filter(user=user, city_id=city_id).order_by('-updated_at')[:50])
    history.reverse()

    labels = [entry.updated_at.strftime('%Y-%m-%d %H:%M') for entry in history]

    if metric == 'humidity':
        data = [entry.humidity for entry in history]
        label = 'Влажность (%)'
        color = 'rgba(54, 162, 235, 1)'
    else:
        data = [entry.temperature for entry in history]
        label = 'Температура (°C)'
        color = 'rgba(255, 99, 132, 1)'

    return render(request, 'weather/chart.html', {
        'labels': json.dumps(labels),
        'data': json.dumps(data),
        'label': label,
        'color': color,
        'city_id': city_id,
        'metric': metric,
    })

class TemperatureChartDataAPI(APIView):
    """Предоставляет данные (в формате JSON) для дальнейшей отрисовки графика погоды на фронте"""
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']

    def get(self, request, city_id):
        history = (
            WeatherHistory.objects.filter(user=request.user, city_id=city_id).order_by('-updated_at')[:100]
        )
        data = [
            {
                'timestamp': entry.updated_at.strftime('%Y-%m-%d %H:%M'),
                'temperature': entry.temperature
            }
            for entry in reversed(history)
        ]
        return Response(data)
