from django.urls import re_path
from shop.websockets.consumers import ShopConsumer

websocket_urlpatterns = [
    re_path(r'ws/shop/$', ShopConsumer.as_asgi()),
]