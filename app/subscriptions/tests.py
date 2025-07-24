import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from django.urls import reverse
from unittest import mock
from app.weather.models import City
from app.subscriptions.models import UserSubscription
from app.subscriptions.serializers import UserSubscriptionSerializer
from app.subscriptions.tasks import update_weather_data, check_weather_threshold

User = get_user_model()

# MODELS
@pytest.mark.django_db
def test_user_subscription_str():
    user = User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass'
    )
    city = City.objects.create(name='Berlin')
    sub = UserSubscription.objects.create(user=user, city=city)

    assert str(sub) == f'{user} subscribed to the city {city}'

# SERIALIZERS
@pytest.mark.django_db
def test_temperature_threshold_validation():
    city = City.objects.create(name='Berlin')
    user = User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass'
    )
    data = {
        'city': city.id,
        'temperature_threshold': -100
    }
    serializer = UserSubscriptionSerializer(data=data)
    serializer.context['request'] = None
    assert not serializer.is_valid()
    assert 'temperature_threshold' in serializer.errors

#  VIEWS
@pytest.mark.django_db
def test_create_subscription():
    user = User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass'
    )
    client = APIClient()
    client.force_authenticate(user=user)
    city = City.objects.create(name='Berlin')

    response = client.post(reverse('usersubscription-list'), {
        'city': city.id,
        'temperature_threshold': 25,
        'temperature_alert_direction': 'above'
    },
    format='json')

    assert response.status_code == 201
    assert response.data['user'] == user.id
    assert response.data['city'] == city.id

# TASKS
@pytest.mark.django_db
@mock.patch('app.subscriptions.tasks.fetch_weather_data')
def test_update_weather_data(mock_fetch_weather_data):
    mock_fetch_weather_data.return_value = {
        'temperature': 30,
        'humidity': 50,
        'pressure': 750,
        'wind_speed': 5,
        'cloudiness': 20,
        'description': 'Clear',
    }
    user = User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass'
    )
    city = City.objects.create(name='Paris')
    UserSubscription.objects.create(user=user, city=city)

    update_weather_data()
    sub = UserSubscription.objects.get(user=user)
    assert float(sub.temperature) == 30
    assert sub.humidity == 50

@pytest.mark.django_db
@mock.patch('app.subscriptions.tasks.send_mail')
def test_check_weather_threshold_sends_email(mock_send_mail):
    user = User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass'
    )
    city = City.objects.create(name='Rome')
    sub = UserSubscription.objects.create(
        user=user, city=city,
        temperature=40,
        temperature_threshold=30,
        temperature_alert_direction='above'
    )
    check_weather_threshold(sub.id)

    mock_send_mail.assert_called_once()
    sub.refresh_from_db()
    assert sub.notified is True
