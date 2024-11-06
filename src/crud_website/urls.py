from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger configuration
schema_view = get_schema_view(
    openapi.Info(
        title="Shop API",
        default_version='v1',
        description="API документация для магазина",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@shop.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API URLs
    path('', include('shop.urls')),
    
    # API Documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), 
         name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), 
         name='schema-redoc'),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), 
         name='schema-json'),
    
    # REST Framework browsable API authentication
    path('api-auth/', include('rest_framework.urls', 
         namespace='rest_framework')),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, 
                         document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, 
                         document_root=settings.MEDIA_ROOT)