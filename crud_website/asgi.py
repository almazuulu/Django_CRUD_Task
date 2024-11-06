# project/asgi.py
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from django.urls import path
from shop.consumers import ShopConsumer  # Ваш consumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

# Определение WebSocket URL patterns
websocket_urlpatterns = [
    path('ws/shop/', ShopConsumer.as_asgi()),
]

# Настройка ASGI приложения
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(websocket_urlpatterns)
        )
    ),
})