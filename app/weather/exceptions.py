from rest_framework import status
from rest_framework.exceptions import APIException


class WeatherServiceUnavailable(APIException):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    default_detail = 'Weather service is temporarily unavailable.'
    default_code = 'weather_service_unavailable'