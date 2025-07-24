import requests
from rest_framework.exceptions import ValidationError
from .serializers import WeatherSerializer
from urllib.parse import urlencode, urljoin
from django.conf import settings
from .exceptions import WeatherServiceUnavailable


def fetch_weather_data(city_name):
    """обращается к api OpenWeatherMap и сохраняет данные о погоде в момент подписки пользователя на определенный город"""
    base_url = settings.OPENWEATHERMAP_API_URL
    path = f"/data/{settings.OPENWEATHERMAP_API_VERSION}/weather"
    full_path = urljoin(base_url, path)

    params = {
        'q': city_name,
        'appid': settings.OPENWEATHERMAP_API_KEY,
        'units': 'metric',
    }
    url = f"{full_path}?{urlencode(params)}"
    response = requests.get(url, timeout=5)

    if response.status_code != 200:
        raise WeatherServiceUnavailable(f"Error OpenWeatherMap: {response.status_code}")

    data = response.json()

    if 'main' not in data:
        raise WeatherServiceUnavailable("Service unavailable")

    weather_data = {
        'temperature': data['main'].get('temp'),
        'humidity': data['main'].get('humidity'),
        'pressure': data['main'].get('pressure'),
        'wind_speed': data.get('wind', {}).get('speed'),
        'cloudiness': data.get('clouds', {}).get('all'),
        'description': data.get('weather', [{}])[0].get('description'),
    }

    serializer = WeatherSerializer(data=weather_data)
    if serializer.is_valid():
        return serializer.validated_data
    else:
        raise ValidationError(serializer.errors)


