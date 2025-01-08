import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

# Import WebSocket URL patterns from different apps
from myapp.chat.routing import websocket_urlpatterns as chat_patterns
from myapp.video_call.routing import websocket_urlpatterns as video_call_patterns
from myapp.voice_message.routing import websocket_urlpatterns as voice_message_patterns

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Cloud_Hoskie.settings')

# Create the Django ASGI application
django_asgi_app = get_asgi_application()

# Combine WebSocket URL patterns
websocket_urlpatterns = chat_patterns + video_call_patterns + voice_message_patterns

# Define the ASGI application
application = ProtocolTypeRouter({
    "http": django_asgi_app,  # HTTP traffic
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns  # Combined WebSocket traffic
        )
    ),
})
