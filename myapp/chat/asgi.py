# chat/asgi.py
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from . import consumers

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cloud_Hoskie.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            # Define the WebSocket URL routing
            path('ws/messaging/<str:username>/<str:recipient_username>/', consumers.ChatConsumer.as_asgi()),
        ])
    ),
})
