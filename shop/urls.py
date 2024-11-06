from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    # ViewSets
    CategoryViewSet,
    ManufacturerViewSet,
    ProductViewSet,
    CustomerViewSet,
    
    # Views
    WebSocketTestView,
)

app_name = 'shop'

# REST API Routers settinsg
router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'manufacturers', ManufacturerViewSet, basename='manufacturer')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'customers', CustomerViewSet, basename='customer')

# URL patterns shops
urlpatterns = [
    # REST API URLs
    path('api/', include(router.urls)),
    
    # WebSocket test page
    path('ws-test/', WebSocketTestView.as_view(), name='ws-test'),
]