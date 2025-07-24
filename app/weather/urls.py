from django.urls import path
from .views import weather_chart_view, TemperatureChartDataAPI

app_name = 'weather'

urlpatterns = [
    path('weather/chart/<int:city_id>/', weather_chart_view, name='weather_chart'),
    path('weather/chart/api/<int:city_id>/', TemperatureChartDataAPI.as_view(), name='temperature_chart_data_api')
]

