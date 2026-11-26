from django.urls import include

import rest_framework.schemas
from django.contrib import admin
from django.http import JsonResponse
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions


def health_check(request):
    return JsonResponse({'status': 'ok'})


schema_view = get_schema_view(
   openapi.Info(
      title="SafeServe API",
      default_version='v1',
      description="System for restaurant managing",
      terms_of_service="https://www.example.com/policies/terms/",
      contact=openapi.Contact(email=""),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('', health_check, name='home'),
    path('admin-k9Xm4pR2/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),

    path('swagger.<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('schema/', rest_framework.schemas.get_schema_view(title='SafeServe API')),
    path('api/v1/auth/', include('dj_rest_auth.urls')),
    #path('api/v1/auth/registration/',include('dj_rest_auth.registration.urls')),

    path('api/v1/restaurant/', include('restaurant.urls'))
]