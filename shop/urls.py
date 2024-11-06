# shop/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api.products import ProductViewSet
from .api.categories import CategoryViewSet
from .api.customers import CustomerViewSet
from .api.manufacturers import ManufacturerViewSet
from .views import WebSocketTestView
from django.views.generic import TemplateView

app_name = 'shop'

# REST API router configuration
router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'customers', CustomerViewSet, basename='customer')
router.register(r'manufacturers', ManufacturerViewSet, basename='manufacturer')

# URL patterns for the shop application
urlpatterns = [
    # API endpoints (v1)
    path('api/v1/', include([
        # Base router URLs
        path('', include(router.urls)),
        
        # Products endpoints
        path('products/', 
             ProductViewSet.as_view({'get': 'list', 'post': 'create'}), 
             name='product-list'),
        path('products/<int:pk>/', 
             ProductViewSet.as_view({
                 'get': 'retrieve',
                 'put': 'update',
                 'patch': 'partial_update',
                 'delete': 'destroy'
             }), 
             name='product-detail'),
        path('products/in-stock/', 
             ProductViewSet.as_view({'get': 'in_stock'}), 
             name='products-in-stock'),
        
        # Categories endpoints
        path('categories/', 
             CategoryViewSet.as_view({'get': 'list', 'post': 'create'}), 
             name='category-list'),
        path('categories/<int:pk>/', 
             CategoryViewSet.as_view({
                 'get': 'retrieve',
                 'put': 'update',
                 'patch': 'partial_update',
                 'delete': 'destroy'
             }), 
             name='category-detail'),
        path('categories/with-products/', 
             CategoryViewSet.as_view({'get': 'with_products'}), 
             name='categories-with-products'),
        
        # Customers endpoints
        path('customers/', 
             CustomerViewSet.as_view({'get': 'list', 'post': 'create'}), 
             name='customer-list'),
        path('customers/<int:pk>/', 
             CustomerViewSet.as_view({
                 'get': 'retrieve',
                 'put': 'update',
                 'patch': 'partial_update',
                 'delete': 'destroy'
             }), 
             name='customer-detail'),
        path('customers/active/', 
             CustomerViewSet.as_view({'get': 'active'}), 
             name='active-customers'),
        
        # Manufacturers endpoints
        path('manufacturers/', 
             ManufacturerViewSet.as_view({'get': 'list', 'post': 'create'}), 
             name='manufacturer-list'),
        path('manufacturers/<int:pk>/', 
             ManufacturerViewSet.as_view({
                 'get': 'retrieve',
                 'put': 'update',
                 'patch': 'partial_update',
                 'delete': 'destroy'
             }), 
             name='manufacturer-detail'),
        path('manufacturers/by-country/', 
             ManufacturerViewSet.as_view({'get': 'by_country'}), 
             name='manufacturers-by-country'),
    ])),
    
    # WebSocket endpoints
    path('ws/test/', WebSocketTestView.as_view(), name='websocket-test'),
    
    # API Documentation
    path('api/docs/', TemplateView.as_view(
        template_name='shop/api_docs.html'
    ), name='api-docs'),
]

# Custom API endpoints patterns (for additional actions)
custom_patterns = [
    # Product related endpoints
    path('api/v1/products/<int:pk>/fans/', 
         ProductViewSet.as_view({'get': 'fans'}), 
         name='product-fans'),
    path('api/v1/products/<int:pk>/update-stock/', 
         ProductViewSet.as_view({'patch': 'update_stock'}), 
         name='update-product-stock'),
    
    # Category related endpoints
    path('api/v1/categories/<int:pk>/products/', 
         CategoryViewSet.as_view({'get': 'products'}), 
         name='category-products'),
    
    # Customer related endpoints
    path('api/v1/customers/<int:pk>/toggle-favorite/', 
         CustomerViewSet.as_view({'post': 'toggle_favorite'}), 
         name='toggle-favorite'),
    path('api/v1/customers/<int:pk>/favorites/', 
         CustomerViewSet.as_view({'get': 'favorites'}), 
         name='customer-favorites'),
    
    # Manufacturer related endpoints
    path('api/v1/manufacturers/<int:pk>/update-contacts/', 
         ManufacturerViewSet.as_view({'patch': 'update_contacts'}), 
         name='update-manufacturer-contacts'),
]

# Adding custom patterns to urlpatterns
urlpatterns.extend(custom_patterns)