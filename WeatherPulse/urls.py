from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from app.weather.views import CityViewSet
from app.subscriptions.views import UserSubscriptionViewSet
from .yasg import urlpatterns as doc_urls  # документация Swagger/OpenAPI

router = DefaultRouter()
router.register(r'cities', CityViewSet)
router.register(r'subscriptions', UserSubscriptionViewSet)

api_patterns = [
    path('', include(router.urls)),
    path('users/', include('app.users.urls')),
    path('weather/', include('app.weather.urls')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_patterns)),  # Весь API под префиксом /api/
]

urlpatterns += doc_urls
