import logging
import requests
from rest_framework.exceptions import ValidationError
from .serializers import WeatherSerializer
from urllib.parse import urlencode, urljoin
from django.conf import settings
from .exceptions import WeatherServiceUnavailable

logger = logging.getLogger('myapp')

def fetch_weather_data(city_name):
    """Обращается к API OpenWeatherMap и сохраняет данные о погоде в момент подписки пользователя на город."""
    base_url = settings.OPENWEATHERMAP_API_URL
    path = f"/data/{settings.OPENWEATHERMAP_API_VERSION}/weather"
    full_path = urljoin(base_url, path)

    params = {
        'q': city_name,
        'appid': settings.OPENWEATHERMAP_API_KEY,
        'units': 'metric',
    }
    url = f"{full_path}?{urlencode(params)}"

    logger.info(f"Запрос погоды для города '{city_name}' к URL: {url}")

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка запроса к OpenWeatherMap для города '{city_name}': {e}", exc_info=True)
        raise WeatherServiceUnavailable(f"Error OpenWeatherMap: {e}")

    try:
        data = response.json()
    except ValueError as e:
        logger.error(f"Ошибка парсинга JSON от OpenWeatherMap для города '{city_name}': {e}", exc_info=True)
        raise WeatherServiceUnavailable("Service returned invalid JSON")

    if 'main' not in data:
        logger.error(f"В ответе OpenWeatherMap отсутствует ключ 'main' для города '{city_name}': {data}")
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
        logger.debug(f"Успешная сериализация данных погоды для города '{city_name}': {serializer.validated_data}")
        return serializer.validated_data
    else:
        logger.error(f"Ошибка сериализации данных погоды для города '{city_name}': {serializer.errors}")
        raise ValidationError(serializer.errors)
