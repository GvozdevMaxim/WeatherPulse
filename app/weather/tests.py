import pytest
from unittest.mock import patch, MagicMock
from rest_framework.exceptions import ValidationError
from rest_framework.test import APIClient
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from app.weather.utils import fetch_weather_data
from app.weather.exceptions import WeatherServiceUnavailable
from app.weather.models import City, WeatherHistory


User = get_user_model()

@pytest.mark.parametrize("status_code", [400, 500])
def test_fetch_weather_data_raises_service_unavailable_on_bad_status(status_code):
    with patch("app.weather.utils.requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = status_code
        mock_get.return_value = mock_response

        with pytest.raises(WeatherServiceUnavailable):
            fetch_weather_data("Moscow")


def test_fetch_weather_data_raises_service_unavailable_if_no_main():
    with patch("app.weather.utils.requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_get.return_value = mock_response

        with pytest.raises(WeatherServiceUnavailable):
            fetch_weather_data("Moscow")


def test_fetch_weather_data_raises_validation_error_if_data_invalid():
    with patch("app.weather.utils.requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "main": {
                "temp": None,
                "humidity": None,
                "pressure": None,
            },
            "wind": {},
            "clouds": {},
            "weather": [{}],
        }
        mock_get.return_value = mock_response

        with pytest.raises(ValidationError):
            fetch_weather_data("Moscow")


def test_fetch_weather_data_returns_valid_data():
    with patch("app.weather.utils.requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "main": {
                "temp": 20.5,
                "humidity": 80,
                "pressure": 1012,
            },
            "wind": {"speed": 5.5},
            "clouds": {"all": 75},
            "weather": [{"description": "clear sky"}],
        }
        mock_get.return_value = mock_response

        data = fetch_weather_data("Moscow")
        assert data['temperature'] == 20.5
        assert data['humidity'] == 80
        assert data['pressure'] == 1012
        assert data['wind_speed'] == 5.5
        assert data['cloudiness'] == 75
        assert data['description'] == "clear sky"


# Тесты для views

@pytest.mark.django_db
def test_city_viewset_list_and_create():
    client = APIClient()

    response = client.post(reverse('city-list'), {'name': 'TestCity', 'country': 'TestCountry'}, format='json')
    assert response.status_code == 201
    city_id = response.data['id']

    response = client.get(reverse('city-list'))
    assert response.status_code == 200
    assert any(city['id'] == city_id for city in response.data)


@pytest.mark.django_db
def test_weather_chart_view_renders(client):
    user = User.objects.create_user(username='gastinhaha', password='pass123')
    city = City.objects.create(name='TestCity')

    for i in range(5):
        WeatherHistory.objects.create(
            user=user,
            city=city,
            temperature=20 + i,
            humidity=50 + i,
            updated_at=timezone.now()
        )

    url = reverse('weather:weather_chart', kwargs={'city_id': city.id})
    response = client.get(url)
    assert response.status_code == 200
    assert b'<canvas' in response.content


@pytest.mark.django_db
def test_temperature_chart_data_api_requires_authentication():
    client = APIClient()
    city = City.objects.create(name='TestCity')

    url = reverse('weather:temperature_chart_data_api', kwargs={'city_id': city.id})

    response = client.get(url)
    assert response.status_code == 401

@pytest.mark.django_db
def test_temperature_chart_data_api_returns_data():
    user = User.objects.create_user(username='testuser', password='pass123')
    city = City.objects.create(name='TestCity')

    WeatherHistory.objects.create(user=user, city=city, temperature=22.5, updated_at=timezone.now())
    WeatherHistory.objects.create(user=user, city=city, temperature=23.0, updated_at=timezone.now())

    client = APIClient()
    client.force_authenticate(user=user)

    url = reverse('weather:temperature_chart_data_api', kwargs={'city_id': city.id})
    response = client.get(url)

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert all('timestamp' in entry and 'temperature' in entry for entry in response.json())
