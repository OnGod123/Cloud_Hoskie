import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import re_path
from live_app import consumers  # Import the consumer directly

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Regular HTTP requests
    "websocket": AuthMiddlewareStack(  # WebSocket connections with auth middleware
        URLRouter([
            # Inline WebSocket URL definition
            re_path(r'ws/live_session/(?P<session_id>\d+)/$', consumers.LiveSessionConsumer.as_asgi()),
        ])
    ),
})
