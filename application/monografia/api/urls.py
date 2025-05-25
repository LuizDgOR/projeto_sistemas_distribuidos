from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from .views import MonografiaViewSet

router = DefaultRouter()
router.register(r'monografias', MonografiaViewSet, basename='monografia')

urlpatterns = [
    # CRUD
    path('', include(router.urls)),
    # endpoint para obter token post
    path('token/', obtain_auth_token, name='api_token_auth'),
    # OpenAPI schema / Swagger UI
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
